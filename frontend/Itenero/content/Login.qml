import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    width: 1920
    height: 1080

    Text {
        id: text1
        x: 878
        y: 145
        width: 165
        height: 80
        text: qsTr("Login")
        font.pixelSize: 30
    }

    TextField {
        id: textField
        x: 471
        y: 354
        width: 475
        height: 75
        opacity: 0.5
        color: "#000000"
        font.pointSize: 20
        placeholderTextColor: "#000000"
        clip: false
        placeholderText: qsTr("Ex: abc@mail.com")
    }

    Text {
        id: text2
        x: 471
        y: 310
        width: 475
        height: 38
        text: qsTr("Email Address:")
        font.pixelSize: 25
    }

    Text {
        id: text3
        x: 1001
        y: 310
        width: 475
        height: 38
        text: qsTr("Password:")
        font.pixelSize: 25
    }

    TextField {
        id: textField1
        x: 1001
        y: 354
        width: 475
        height: 75
        opacity: 0.5
        visible: false
        color: "#000000"
        placeholderText: qsTr("Password must be 8-16 characters")
        hoverEnabled: true
        font.pointSize: 20
        placeholderTextColor: "#000000"
        clip: false
    }
}
