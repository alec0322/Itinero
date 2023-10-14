import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    width: 1920
    height: 1080

    Text {
        id: text1
        x: 885
        y: 170
        width: 235
        height: 70
        text: qsTr("Create Account")
        font.pixelSize: 30
    }

    TextField {
        id: textField
        x: 487
        y: 450
        width: 475
        height: 75
        opacity: 0.5
        color: "#000000"
        clip: false
        placeholderTextColor: "#000000"
        font.pointSize: 20
        placeholderText: qsTr("Ex: abc@mail.com")
    }

    Text {
        id: text2
        x: 487
        y: 411
        width: 475
        height: 38
        text: qsTr("Email Address:")
        font.pixelSize: 25
    }

    Text {
        id: text3
        x: 487
        y: 265
        width: 475
        height: 38
        text: qsTr("First Name:")
        font.pixelSize: 25
    }

    TextField {
        id: textField1
        x: 487
        y: 309
        width: 475
        height: 75
        opacity: 0.5
        color: "#000000"
        font.pointSize: 20
        placeholderTextColor: "#000000"
        clip: false
        placeholderText: qsTr("Ex: John")
    }

    TextField {
        id: textField2
        x: 1075
        y: 450
        width: 475
        height: 75
        opacity: 0.5
        color: "#000000"
        font.pointSize: 20
        placeholderTextColor: "#000000"
        clip: false
        placeholderText: qsTr("Password must be 8-16 characters")
    }

    Text {
        id: text4
        x: 1075
        y: 411
        width: 475
        height: 38
        text: qsTr("Password:")
        font.pixelSize: 25
    }

    Text {
        id: text5
        x: 1075
        y: 265
        width: 475
        height: 38
        text: qsTr("Last Name:")
        font.pixelSize: 25
    }

    TextField {
        id: textField3
        x: 1075
        y: 309
        width: 475
        height: 75
        opacity: 0.5
        color: "#000000"
        font.pointSize: 20
        placeholderTextColor: "#000000"
        clip: false
        placeholderText: qsTr("Ex: Smith")
    }
}
