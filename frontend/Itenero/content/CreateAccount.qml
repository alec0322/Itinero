import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    width: 1920
    height: 1080

    Text {
        id: text1
        x: 748
        y: 193
        width: 630
        height: 122
        text: qsTr("Create your account")
        font.pixelSize: 30
    }

    Text {
        id: text2
        x: 569
        y: 321
        width: 191
        height: 54
        text: qsTr("First Name:")
        font.pixelSize: 25
    }

    Text {
        id: text3
        x: 569
        y: 518
        width: 191
        height: 54
        text: qsTr("Email Address:")
        font.pixelSize: 25
    }

    Text {
        id: text4
        x: 991
        y: 321
        width: 191
        height: 54
        text: qsTr("Last Name:")
        font.pixelSize: 25
    }

    Text {
        id: text5
        x: 991
        y: 518
        width: 191
        height: 54
        text: qsTr("Password:")
        font.pixelSize: 25
    }

    TextField {
        id: textField
        x: 569
        y: 381
        opacity: 1
        placeholderText: qsTr("Ex: John")
    }

    TextField {
        id: textField1
        x: 569
        y: 590
        opacity: 1
        placeholderText: qsTr("Ex: abc@mail.com")
    }

    TextField {
        id: textField2
        x: 991
        y: 381
        opacity: 1
        placeholderText: qsTr("Ex: Smith")
    }

    TextField {
        id: passWord
        x: 991
        y: 590
        opacity: 1
        passwordCharacter: "●0"
        echoMode: TextInput.Password
        placeholderText: qsTr("8-16 characters")
    }

    Button {
        id: button
        x: 809
        y: 707
        text: qsTr("Submit")
    }
}
