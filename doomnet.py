

import sys
import ipaddress
from PyQt5 import QtWidgets, QtCore

# Lógica funcional del programa, basada en métodos @staticmethod, como bien se puede observar pero, como no todos son agraciados en conexiones neuronales...

class NetworkCalculator:
    @staticmethod
    def network_info(cidr: str):
        net = ipaddress.ip_network(cidr, strict=False)
        return {
            "network": str(net.network_address),
            "broadcast": str(net.broadcast_address),
            "netmask": str(net.netmask),
            "hosts": net.num_addresses - (2 if net.version == 4 and net.prefixlen < 31 else 0),
            "first_host": str(list(net.hosts())[0]) if net.num_addresses > 2 else "N/A",
            "last_host": str(list(net.hosts())[-1]) if net.num_addresses > 2 else "N/A",
        }

    @staticmethod
    def subnet_calculation(cidr: str, new_prefix: int):
        net = ipaddress.ip_network(cidr, strict=False)
        return [str(subnet) for subnet in net.subnets(new_prefix=new_prefix)]

    @staticmethod
    def ip_range(start_ip: str, end_ip: str):
        start = ipaddress.ip_address(start_ip)
        end = ipaddress.ip_address(end_ip)
        return [str(ipaddress.ip_address(ip)) for ip in range(int(start), int(end)+1)]

    @staticmethod
    def vlan_segmentation(base_cidr: str, vlan_count: int):
        net = ipaddress.ip_network(base_cidr, strict=False)
        new_prefix = net.prefixlen + (vlan_count.bit_length() - 1)
        return [str(subnet) for subnet in net.subnets(new_prefix=new_prefix)]

# Bueno, a continuación, la clase que utiliza QtWidgets, lo dice todo todito...GUI MTF-style.

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DoomNet - The Doomguy has arrived.")
        self.resize(700, 500)

        
        self.setStyleSheet("""
            QWidget {
                background-color: #0d0d0d;
                color: #ffffff;
            }

            QTabWidget::pane {
                border: 1px solid #8a5cff;
            }

            QTabBar::tab {
                background: #1a1a1a;
                color: white;
                padding: 6px;
                border: 1px solid #8a5cff;
            }

            QTabBar::tab:selected {
                background: #8a5cff;
            }

            QPushButton {
                background-color: #8a5cff;
                color: white;
                padding: 6px;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #a87cff;
            }

            QLineEdit, QTextEdit {
                background-color: #1a1a1a;
                border: 1px solid #8a5cff;
                padding: 6px;
                color: white;
            }

            QLineEdit:focus {
                border: 1px solid #c2a3ff;
                background-color: #222222;
            }

            QTextEdit {
                selection-background-color: #8a5cff;
            }
        """)

        self.tabs = QtWidgets.QTabWidget()

        self.tabs.addTab(self.network_tab(), "Network Info")
        self.tabs.addTab(self.subnet_tab(), "Subnetting")
        self.tabs.addTab(self.range_tab(), "IP Range")
        self.tabs.addTab(self.vlan_tab(), "VLAN Segmentation")
        self.tabs.addTab(self.tutorial_tab(), "Tutorials")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    # Tab Tab Tab Tab Tab Tab.

    def network_tab(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        self.net_input = QtWidgets.QLineEdit()
        self.net_input.setPlaceholderText("192.168.1.0/24")

        btn = QtWidgets.QPushButton("Calculate")
        btn.clicked.connect(self.calculate_network)

        self.net_output = QtWidgets.QTextEdit()

        layout.addWidget(self.net_input)
        layout.addWidget(btn)
        layout.addWidget(self.net_output)
        tab.setLayout(layout)
        return tab

    def subnet_tab(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        self.subnet_input = QtWidgets.QLineEdit()
        self.subnet_input.setPlaceholderText("192.168.1.0/24")

        self.prefix_input = QtWidgets.QLineEdit()
        self.prefix_input.setPlaceholderText("New prefix (e.g. 26)")

        btn = QtWidgets.QPushButton("Subnet")
        btn.clicked.connect(self.calculate_subnet)

        self.subnet_output = QtWidgets.QTextEdit()

        layout.addWidget(self.subnet_input)
        layout.addWidget(self.prefix_input)
        layout.addWidget(btn)
        layout.addWidget(self.subnet_output)
        tab.setLayout(layout)
        return tab

    def range_tab(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        self.range_start = QtWidgets.QLineEdit()
        self.range_start.setPlaceholderText("Start IP")

        self.range_end = QtWidgets.QLineEdit()
        self.range_end.setPlaceholderText("End IP")

        btn = QtWidgets.QPushButton("Generate Range")
        btn.clicked.connect(self.calculate_range)

        self.range_output = QtWidgets.QTextEdit()

        layout.addWidget(self.range_start)
        layout.addWidget(self.range_end)
        layout.addWidget(btn)
        layout.addWidget(self.range_output)
        tab.setLayout(layout)
        return tab

    def vlan_tab(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        self.vlan_input = QtWidgets.QLineEdit()
        self.vlan_input.setPlaceholderText("192.168.0.0/24")

        self.vlan_count = QtWidgets.QLineEdit()
        self.vlan_count.setPlaceholderText("Number of VLANs")

        btn = QtWidgets.QPushButton("Segment VLAN")
        btn.clicked.connect(self.calculate_vlan)

        self.vlan_output = QtWidgets.QTextEdit()

        layout.addWidget(self.vlan_input)
        layout.addWidget(self.vlan_count)
        layout.addWidget(btn)
        layout.addWidget(self.vlan_output)
        tab.setLayout(layout)
        return tab

    def tutorial_tab(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        tutorial_text = QtWidgets.QTextEdit()
        tutorial_text.setReadOnly(True)

        tutorial_text.setText("""
=== NETWORK INFO ===
Calcula datos de una red: dirección de red, broadcast, máscara y hosts.

=== SUBNETTING ===
Divide una red en subredes más pequeñas usando un nuevo prefijo.

=== IP RANGE ===
Genera un rango completo de direcciones IP entre dos valores.

=== VLAN SEGMENTATION ===
Divide una red base en múltiples redes para segmentación VLAN.

""")

        layout.addWidget(tutorial_text)
        tab.setLayout(layout)
        return tab

    # El motor de cálculo, la salchipapa de la máquina.

    def calculate_network(self):
        try:
            data = NetworkCalculator.network_info(self.net_input.text())
            self.net_output.setText("\n".join(f"{k}: {v}" for k, v in data.items()))
        except Exception as e:
            self.net_output.setText(str(e))

    def calculate_subnet(self):
        try:
            subnets = NetworkCalculator.subnet_calculation(
                self.subnet_input.text(), int(self.prefix_input.text())
            )
            self.subnet_output.setText("\n".join(subnets))
        except Exception as e:
            self.subnet_output.setText(str(e))

    def calculate_range(self):
        try:
            ips = NetworkCalculator.ip_range(
                self.range_start.text(), self.range_end.text()
            )
            self.range_output.setText("\n".join(ips))
        except Exception as e:
            self.range_output.setText(str(e))

    def calculate_vlan(self):
        try:
            vlans = NetworkCalculator.vlan_segmentation(
                self.vlan_input.text(), int(self.vlan_count.text())
            )
            self.vlan_output.setText("\n".join(vlans))
        except Exception as e:
            self.vlan_output.setText(str(e))


# -----------------------------
# Main
# -----------------------------

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
