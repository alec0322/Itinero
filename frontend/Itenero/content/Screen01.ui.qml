/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick 6.5
import QtQuick.Controls 6.5
import Itenero

Rectangle {
    width: Constants.width
    height: Constants.height
    color: "#c2c2c2"


    Text {
        id: text1
        x: 850
        y: 344
        width: 220
        height: 44
        text: qsTr("ITENERO")
        font.letterSpacing: 4
        font.pixelSize: 17
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        style: Text.Normal
        font.styleName: "Bold Italic"
        font.family: "Times New Roman"
    }

    Button {
        id: button
        x: 813
        y: 433
        opacity: 1
        text: qsTr("Create Account")
        transformOrigin: Item.Center
        icon.width: 24
        display: AbstractButton.TextBesideIcon
        highlighted: true
        flat: false
        clip: false
    }

    Button {
        id: button1
        x: 999
        y: 433
        text: qsTr("Login")
        icon.color: "#f94043e6"
        highlighted: true
    }
}
