import sys
import time
import random
from PyQt5 import QtWidgets, QtCore
from projeto import ProxyViewerImproved, ProxyViewer

class ProxyValidationThread(QtCore.QThread):
    validation_finished = QtCore.pyqtSignal(list)

    def __init__(self, viewer):
        super().__init__()
        self.viewer = viewer

    def run(self):
        valid_proxies = self.viewer.validate_all_proxies()
        self.validation_finished.emit(valid_proxies)

class StreamViewerApp(QtWidgets.QMainWindow):
    update_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.viewer = None
        self.thread = None
        self.init_ui()
        self.update_signal.connect(self.update_log)

    def update_log(self, message):
        self.log_output.append(f"[{time.strftime('%H:%M:%S')}] {message}")

    def stop_viewer(self):
        if self.viewer:
            self.viewer.active = False
        if hasattr(self, 'thread') and self.thread:
            self.thread.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.update_signal.emit("Visualizações interrompidas")

    def init_ui(self):
        self.setWindowTitle("Stream Viewer Manager")
        self.setGeometry(100, 100, 600, 400)

        self.proxy_input = QtWidgets.QTextEdit()
        self.proxy_input.setPlaceholderText("Insira proxies (um por linha)")

        # Preenche automaticamente com proxies fictícios para testes
        try:
            from projeto import generate_test_proxies
            test_proxies = generate_test_proxies(50)
            self.proxy_input.setPlainText("\n".join(test_proxies))
        except Exception:
            pass

        self.stream_url_input = QtWidgets.QLineEdit()
        self.stream_url_input.setPlaceholderText("URL da transmissão")

        self.views_input = QtWidgets.QSpinBox()
        self.views_input.setRange(1, 1000)
        self.views_input.setValue(10)

        self.log_output = QtWidgets.QTextEdit()
        self.log_output.setReadOnly(True)

        self.selenium_checkbox = QtWidgets.QCheckBox("Usar Selenium (visualização real)")
        self.selenium_checkbox.setChecked(False)

        self.test_mode_checkbox = QtWidgets.QCheckBox("Modo Teste (ignorar validação de proxies)")
        self.test_mode_checkbox.setChecked(False)

        self.start_btn = QtWidgets.QPushButton("Iniciar Visualizações")
        self.start_btn.clicked.connect(self.start_viewer)

        self.stop_btn = QtWidgets.QPushButton("Parar")
        self.stop_btn.clicked.connect(self.stop_viewer)
        self.stop_btn.setEnabled(False)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout()

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Proxies:", self.proxy_input)
        form_layout.addRow("URL da Stream:", self.stream_url_input)
        form_layout.addRow("Nº de Visualizações:", self.views_input)

        layout.addLayout(form_layout)
        layout.addWidget(self.selenium_checkbox)
        layout.addWidget(self.test_mode_checkbox)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(QtWidgets.QLabel("Log de Atividade:"))
        layout.addWidget(self.log_output)

        central_widget.setLayout(layout)


    def start_viewer(self):
        proxies = [p.strip() for p in self.proxy_input.toPlainText().split('\n') if p.strip()]
        stream_url = self.stream_url_input.text().strip()
        num_views = self.views_input.value()

        if not proxies or not stream_url:
            QtWidgets.QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return

        use_selenium = self.selenium_checkbox.isChecked()
        test_mode = self.test_mode_checkbox.isChecked()
        self.viewer = ProxyViewerImproved(proxies)
        self._pending_stream_url = stream_url
        self._pending_num_views = num_views
        self._pending_use_selenium = use_selenium
        self._pending_test_mode = test_mode
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        if test_mode:
            # Em modo teste, considera todos os proxies como válidos
            self.on_proxies_validated(proxies)
        else:
            self.log_output.append("Validando proxies...")
            self.validation_thread = ProxyValidationThread(self.viewer)
            self.validation_thread.validation_finished.connect(self.on_proxies_validated)
            self.validation_thread.start()

    def on_proxies_validated(self, valid_proxies):
        num_views = self._pending_num_views
        stream_url = self._pending_stream_url
        use_selenium = self._pending_use_selenium
        if len(valid_proxies) < num_views:
            QtWidgets.QMessageBox.warning(self, "Erro", f"Proxies válidos insuficientes para {num_views} visualizações. Proxies válidos encontrados: {len(valid_proxies)}")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return
        self.viewer.valid_proxies = valid_proxies
        self.thread = ViewerThread(self.viewer, stream_url, num_views, use_selenium)
        self.thread.update_signal.connect(self.update_log)
        self.thread.finished.connect(self.on_thread_finished)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.thread.start()

    def on_thread_finished(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def stop(self):
        self._is_running = False

# Adaptação do ProxyViewerImproved para aceitar timeout customizado
    
    
    def update_log(self, message):
        self.log_output.append(f"[{time.strftime('%H:%M:%S')}] {message}")

class ViewerThread(QtCore.QThread):
    update_signal = QtCore.pyqtSignal(str)
    
    def __init__(self, viewer, stream_url, num_views, use_selenium=False):
        super().__init__()
        self.viewer = viewer
        self.stream_url = stream_url
        self.num_views = num_views
        self._is_running = True
        self.use_selenium = use_selenium

    def run(self):
        try:
            for i in range(self.num_views):
                if not self._is_running or not getattr(self.viewer, 'active', True):
                    self.update_signal.emit("Execução interrompida pelo usuário.")
                    break
                if i < len(self.viewer.valid_proxies):
                    proxy = self.viewer.valid_proxies[i]
                    if self.use_selenium and hasattr(self.viewer, 'simulate_selenium_view'):
                        try:
                            self.viewer.simulate_selenium_view(proxy, self.stream_url)
                            self.update_signal.emit(f"[SELENIUM] Visualização {i+1} via {proxy} na live {self.stream_url} (SUCESSO)")
                        except Exception as e:
                            self.update_signal.emit(f"[SELENIUM] Visualização {i+1} via {proxy} na live {self.stream_url} (FALHA: {str(e)})")
                    elif hasattr(self.viewer, 'simulate_human_view'):
                        try:
                            self.viewer.simulate_human_view(proxy, self.stream_url)
                            self.update_signal.emit(f"Visualização {i+1} via {proxy} na live {self.stream_url} (SUCESSO)")
                        except Exception as e:
                            self.update_signal.emit(f"Visualização {i+1} via {proxy} na live {self.stream_url} (FALHA: {str(e)})")
                    else:
                        self.update_signal.emit(f"Proxy {proxy} válido, mas método de simulação não encontrado.")
                else:
                    self.update_signal.emit("Proxies insuficientes para todas as visualizações")
                    break
                time.sleep(random.uniform(2, 10))
        except Exception as e:
            self.update_signal.emit(f"Erro: {str(e)}")

    def stop(self):
        self._is_running = False

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StreamViewerApp()
    window.show()
    sys.exit(app.exec_())
