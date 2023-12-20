import sys
import capstone
import pygraphviz as pgv
from PIL import Image
from io import BytesIO
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QFileDialog, QGraphicsScene, QGraphicsView


class CodeAnalysisTool(QMainWindow):
    def __init__(self):
        super(CodeAnalysisTool, self).__init__()

        self.setWindowTitle("Code Analysis Tool")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.txt_code = QTextEdit(self.central_widget)
        self.layout.addWidget(self.txt_code)

        self.btn_disassemble = QPushButton("Disassemble", self.central_widget)
        self.btn_disassemble.clicked.connect(self.disassemble_code)
        self.layout.addWidget(self.btn_disassemble)

        self.btn_analyze_flow = QPushButton("Analyze Control Flow", self.central_widget)
        self.btn_analyze_flow.clicked.connect(self.analyze_control_flow)
        self.layout.addWidget(self.btn_analyze_flow)

        self.view = QGraphicsView(self.central_widget)
        self.layout.addWidget(self.view)

        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

    def disassemble_code(self):
        code = self.txt_code.toPlainText()
        if not code:
            return

        disassembled_code = self.disassemble(code)
        self.txt_code.setPlainText(disassembled_code)

    def analyze_control_flow(self):
        code = self.txt_code.toPlainText()
        if not code:
            return

        graph = self.build_control_flow_graph(code)
        self.visualize_control_flow(graph)

    def disassemble(self, code):
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        disassembled_code = ""
        for i in md.disasm(code.encode(), 0x1000):
            disassembled_code += f"0x{i.address:x}:\t{i.mnemonic} {i.op_str}\n"
        return disassembled_code

    def build_control_flow_graph(self, code):
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        graph = pgv.AGraph(directed=True)

        nodes = set()
        for i in md.disasm(code.encode(), 0x1000):
            nodes.add((i.address, f"{i.mnemonic} {i.op_str}"))

        for node in nodes:
            graph.add_node(node[0], label=node[1])

        addresses = [i.address for i in md.disasm(code.encode(), 0x1000)]
        for i in range(len(addresses) - 1):
            graph.add_edge(addresses[i], addresses[i + 1])

        return graph

    def visualize_control_flow(self, graph):
        if graph is not None:
            graph.layout(prog='dot')
            self.scene.clear()

        # Save the graph to a PNG image
            image_path = 'graph.png'
            graph.draw(image_path, format='png', prog='dot')

        # Load the PNG image using PIL (Pillow)
            img = Image.open(image_path)
            img_byte_array = BytesIO()
            img.save(img_byte_array, format='PNG')
        
        # Use QPixmap from QtGui
            #pixmap = QtGui.QPixmap()
            #pixmap.loadFromData(img_byte_array.getvalue())

        # Display the image in the QGraphicsView
            self.scene.addPixmap(pixmap)
            self.view.setScene(self.scene)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    code_analysis_tool = CodeAnalysisTool()
    code_analysis_tool.show()
    sys.exit(app.exec_())
