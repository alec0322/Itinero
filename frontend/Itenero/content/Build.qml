import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    width: 1920
    height: 1080

    Text {
        id: text1
        x: 676
        y: 124
        width: 348
        height: 61
        text: qsTr("Lets build your itenerary!")
        font.pixelSize: 30
    }

    TextField {
        id: cityField
        x: 720
        y: 264
        placeholderText: qsTr("Ex: Miami")
    }

    Text {
        id: text2
        x: 720
        y: 224
        width: 200
        height: 49
        text: qsTr("Enter a city:")
        font.pixelSize: 20
    }

    Button {
        id: button
        x: 720
        y: 346
        text: qsTr("Submit")
    }
}
