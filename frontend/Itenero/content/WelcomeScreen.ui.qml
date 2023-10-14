/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick 6.5
import QtQuick.Controls 6.5
import Itenero
import FlowView

Rectangle {
    id: rectangle
    width: Constants.width
    height: Constants.height

    color: Constants.backgroundColor

    Text {
        id: text1
        x: 777
        y: 312
        width: 99
        height: 37
        text: qsTr("ITENERO")
        font.letterSpacing: 4
        font.pixelSize: 30
        horizontalAlignment: Text.AlignHCenter
    }

    Button {
        id: createAccount
        x: 682
        y: 424
        text: "Create account"
        spacing: 8
        highlighted: true
        checkable: false
        autoExclusive: false
        display: AbstractButton.TextBesideIcon

        Connections {
            target: createAccount
            onClicked: rectangle.visible = true
        }
    }

    Button {
        id: login
        x: 859
        y: 424
        text: qsTr("Log-In")
        spacing: 8
        highlighted: true
        flat: false
    }

    Connections {
        target: rectangle
        onActiveFocusChanged: createAccount.toggle()
    }
}


