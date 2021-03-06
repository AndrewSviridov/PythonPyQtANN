
import sys, random

from functools import partial

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from ANN.Net import Net


class Controller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700, 100, 900, 700)

        self.l0inputs = []
        self.l0outputs = []
        self.l0wsum = QLineEdit(self)

        self.synapse_buttonsL0L1 = {}

        self.l1inputs = []
        self.l1outputs = []
        self.l1wsum = QLineEdit(self)

        self.synapse_buttonsL1L2 = {}

        self.l2inputs = []
        self.l2outputs = []

        self.expected_v = QLineEdit(self)
        self.delta_v = QLineEdit(self)
        self.MSE_v = QLineEdit(self)
        self.delta_gradient_v = QLineEdit(self)



        self.delta_printbox = QLineEdit(self)



        self.load_inputs_button = QPushButton(self)
        self.load_inputs_button.clicked.connect(m_net.load_inputs)
        self.forward_propL0L1_button = QPushButton(self)
        self.forward_propL0L1_button.clicked.connect(m_net.forward_propL0L1)
        self.forward_propL1L2_button = QPushButton(self)
        self.forward_propL1L2_button.clicked.connect(m_net.forward_propL1L2)
        self.calculate_MSE_and_deltagrad_button = QPushButton(self)
        self.calculate_MSE_and_deltagrad_button.clicked.connect(m_net.calculate_MSE_and_deltagradient)
        self.back_propL2L1_button = QPushButton(self)
        self.back_propL2L1_button.clicked.connect(m_net.back_propL2L1)
        self.back_propL1L0_button = QPushButton(self)
        self.back_propL1L0_button.clicked.connect(m_net.back_propL1L0)
        self.update_weights_button = QPushButton(self)
        self.update_weights_button.clicked.connect(m_net.update_weights)

        self.initialize_and_draw_lineEdits_and_buttons()
        self.initialize_buttons()

        for i in range(0, 2):
            for j in range(0, 4):
                self.synapse_buttonsL0L1[i, j].clicked.connect(partial(self.delta_print, 0, i, j))

        for k in range(0, 4):
            self.synapse_buttonsL1L2[k, 0].clicked.connect(partial(self.delta_print, 1, k, 0))


        self.show()


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_neurons(qp)
        self.draw_synapses_and_labels(qp)
        self.update_lineEdits_and_buttons()

        qp.end()

    def draw_neurons(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)

        #draw first layer
        for i in range(0, 3):
            c = m_net.get_coordinates(m_net.get_neuron(0, i))
            qp.drawEllipse(c[0] - 25, c[1] - 25, 50, 50)

        # draw second layer
        for i in range(0, 5):
            c = m_net.get_coordinates(m_net.get_neuron(1, i))
            qp.drawEllipse(c[0] - 25, c[1] - 25, 50, 50)

        # draw third layer
        for i in range(0, 2):
            c = m_net.get_coordinates(m_net.get_neuron(2, i))
            qp.drawEllipse(c[0] - 25, c[1] - 25, 50, 50)

    def draw_synapses_and_labels(self, qp):
        pen = QPen(Qt.black, 1, Qt.DashLine)
        qp.setPen(pen)

        qp.drawLine(175, 225, 210, 200)
        qp.drawLine(175, 225, 210, 220)
        qp.drawLine(175, 225, 210, 240)
        qp.drawLine(175, 225, 210, 260)

        qp.drawLine(175, 325, 210, 295)
        qp.drawLine(175, 325, 210, 315)
        qp.drawLine(175, 325, 210, 335)
        qp.drawLine(175, 325, 210, 355)

        qp.drawLine(260, 200, 310, 125)
        qp.drawLine(260, 220, 310, 225)
        qp.drawLine(260, 240, 310, 325)
        qp.drawLine(260, 260, 310, 425)

        qp.drawLine(260, 300, 310, 125)
        qp.drawLine(260, 320, 310, 225)
        qp.drawLine(260, 340, 310, 325)
        qp.drawLine(260, 360, 310, 425)

        qp.drawLine(460, 125, 510, 125)
        qp.drawLine(460, 225, 510, 225)
        qp.drawLine(460, 325, 510, 325)
        qp.drawLine(460, 425, 510, 425)

        qp.drawLine(555, 125, 625, 275)
        qp.drawLine(555, 225, 625, 275)
        qp.drawLine(555, 325, 625, 275)
        qp.drawLine(555, 425, 625, 275)

        qp.drawText(10, 210, "input")
        qp.drawText(125, 210, "output")
        qp.drawText(210, 180, "synapses")
        qp.drawText(210, 140, "--")

        qp.drawText(310, 110, "input")
        qp.drawText(425, 110, "output")
        qp.drawText(510, 110, "synapses")
        qp.drawText(510, 70, "--")

        qp.drawText(610, 260, "input")
        qp.drawText(730, 260, "output")
        qp.drawText(780, 260, "expected")
        qp.drawText(845, 260, "delta")
        qp.drawText(780, 305, "MSE")
        qp.drawText(845, 305, "deltagrad")

    def initialize_buttons(self):
        self.load_inputs_button.setGeometry(10, 570, 100, 60)
        self.load_inputs_button.setText("Load inp")
        self.forward_propL0L1_button.setGeometry(200, 570, 100, 60)
        self.forward_propL0L1_button.setText("F-propL1")
        self.forward_propL1L2_button.setGeometry(500, 570, 100, 60)
        self.forward_propL1L2_button.setText("F-propL2")
        self.calculate_MSE_and_deltagrad_button.setGeometry(700, 570, 100, 60)
        self.calculate_MSE_and_deltagrad_button.setText("Calc MSE, delta")
        self.back_propL2L1_button.setGeometry(500, 630, 100, 60)
        self.back_propL2L1_button.setText("B-propL2")
        self.back_propL1L0_button.setGeometry(200, 630, 100, 60)
        self.back_propL1L0_button.setText("B-propL1")
        self.update_weights_button.setGeometry(10, 630, 100, 60)
        self.update_weights_button.setText("Update")

    def initialize_and_draw_lineEdits_and_buttons(self):
        #first layer
        for i in range(0, 2):
            c = m_net.get_coordinates(m_net.get_neuron(0, i))

            #inputs
            my_line_edit_in = QLineEdit(self)
            my_line_edit_in.setGeometry(c[0] - 90, c[1] - 10, 60, 20)
            self.l0inputs.append([i, my_line_edit_in])

            #outputs
            my_line_edit_out = QLineEdit(self)
            my_line_edit_out.setGeometry(c[0] + 25, c[1] - 10, 50, 20)
            self.l0outputs.append([i, my_line_edit_out])

            #weights
            for j in range(0, 4):
                my_line_edit_w = QPushButton(self)
                my_line_edit_w.setGeometry(c[0] + 110, c[1] - 40 + (22 * j), 50, 20)
                self.synapse_buttonsL0L1[i, j] = my_line_edit_w

        c = m_net.get_coordinates(m_net.get_neuron(0, 0))
        self.l0wsum.setGeometry(c[0] + 110, c[1] - 80, 50, 20)


        #second layer
        for i in range(0, 4):
            c = m_net.get_coordinates(m_net.get_neuron(1, i))

            #inputs
            my_line_edit_in = QLineEdit(self)
            my_line_edit_in.setGeometry(c[0] - 90, c[1] - 10, 60, 20)
            self.l1inputs.append([i, my_line_edit_in])

            #outputs
            my_line_edit_out = QLineEdit(self)
            my_line_edit_out.setGeometry(c[0] + 25, c[1] - 10, 50, 20)
            self.l1outputs.append([i, my_line_edit_out])

            #weights
            my_line_edit_w = QPushButton(self)
            my_line_edit_w.setGeometry(c[0] + 110, c[1] - 10, 50, 20)
            self.synapse_buttonsL1L2[i, 0] = my_line_edit_w


        c = m_net.get_coordinates(m_net.get_neuron(1, 0))
        self.l1wsum = QLineEdit(self)
        self.l1wsum.setGeometry(c[0] + 110, c[1] - 50, 50, 20)



        #third layer
        for i in range(0, 1):
            c = m_net.get_coordinates(m_net.get_neuron(2, i))

            #inputs
            my_line_edit_in = QLineEdit(self)
            my_line_edit_in.setGeometry(c[0] - 90, c[1] - 10, 60, 20)
            self.l2inputs.append([i, my_line_edit_in])

            #outputs
            my_line_edit_out = QLineEdit(self)
            my_line_edit_out.setGeometry(c[0] + 25, c[1] - 10, 50, 20)
            self.l2outputs.append([i, my_line_edit_out])


        #draw expected output and error
        self.expected_v.setGeometry(780, 265, 50, 20)
        self.MSE_v.setGeometry(780, 310, 50, 20)
        self.delta_v.setGeometry(840, 265, 50, 20)
        self.delta_gradient_v.setGeometry(840, 310, 50, 20)



        self.delta_printbox.setGeometry(650, 10, 100, 100)
        self.delta_printbox.setFont(QFont("Times", 12))

    def update_lineEdits_and_buttons(self):

        #update first layer
        synapses = getattr(m_net, 'synapsesL0L1')

        for i in range(0, 2):
            #input
            input = m_net.get_input(m_net.get_neuron(0, i))
            QLineEdit.setText(self.l0inputs[i][1], str(round(input, 3)))

            #outputs
            output = m_net.get_output(m_net.get_neuron(0, i))
            QLineEdit.setText(self.l0outputs[i][1], str(round(output, 3)))

            #weights
            for j in range(0, 4):
                weight = getattr(synapses[i, j], 'weight')
                QPushButton.setText(self.synapse_buttonsL0L1[i, j], str(weight))


        # update second layer
        synapses = getattr(m_net, 'synapsesL1L2')

        for i in range(0, 4):

            # input
            input = m_net.get_input(m_net.get_neuron(1, i))
            QLineEdit.setText(self.l1inputs[i][1], str(round(input, 3)))

            # outputs
            output = m_net.get_output(m_net.get_neuron(1, i))
            QLineEdit.setText(self.l1outputs[i][1], str(round(output, 3)))

            # weights
            weight = getattr(synapses[i, 0], 'weight')
            QPushButton.setText(self.synapse_buttonsL1L2[i, 0], str(weight))


        # update third layer

        for i in range(0, 1):

            # input
            input = m_net.get_input(m_net.get_neuron(2, i))
            QLineEdit.setText(self.l2inputs[i][1], str(round(input, 3)))

            # outputs
            output = m_net.get_output(m_net.get_neuron(2, i))
            QLineEdit.setText(self.l2outputs[i][1], str(round(output, 3)))

        QLineEdit.setText(self.expected_v, str(round(getattr(m_net, 'expected'), 3)))
        QLineEdit.setText(self.MSE_v, str(round(getattr(m_net, 'MSE'), 3)))
        QLineEdit.setText(self.delta_v, str(round(getattr(m_net, 'delta'), 3)))
        QLineEdit.setText(self.delta_gradient_v, str(round(getattr(m_net, 'deltagradientL2'), 3)))

    def delta_print(self, layerIndex, i, j):
        if layerIndex == 0:
            deltaweight = getattr(m_net.synapsesL0L1[i, j], 'deltaweight')
            self.delta_printbox.setText(str("Delta_w:" + str(round(deltaweight, 3))))
        else:
            deltaweight = getattr(m_net.synapsesL1L2[i, j], 'deltaweight')
            self.delta_printbox.setText(str("Delta_w:" + str(round(deltaweight, 3))))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    m_net = Net()
    m_controller = Controller()
    print("EOF ")
    sys.exit(app.exec_())






