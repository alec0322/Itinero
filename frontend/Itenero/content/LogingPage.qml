import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    width: 1920
    height: 1080

    Text {
        id: text1
        x: 800
        y: 176
        width: 218
        height: 57
        text: qsTr("Log-in")
        font.pixelSize: 30
    }

    Text {
        id: text3
        x: 533
        y: 321
        width: 191
        height: 54
        text: qsTr("Email Address:")
        font.pixelSize: 25
    }

    Text {
        id: text5
        x: 955
        y: 321
        width: 191
        height: 54
        text: qsTr("Password:")
        font.pixelSize: 25
    }

    TextField {
        id: textField1
        x: 533
        y: 393
        opacity: 1
        placeholderText: qsTr("Ex: abc@mail.com")
    }

    TextField {
        id: textField3
        x: 955
        y: 393
        opacity: 1
        placeholderText: qsTr("8-16 characters")
        passwordCharacter: "●0"
        echoMode: TextInput.Password
    }

    Button {
        id: button
        x: 785
        y: 513
        text: qsTr("Submit")
    }
}
