#Specify target exec name
TARGET = QuizGUI

# Specify source
SOURCES += \
    src/main.cpp \
	src/MCquestion.cpp \
	src/optionWidget.cpp

# Specify any headers
HEADERS += \
	src/MCquestion.h \
	GeneratedFiles/ui_MCquestion.h \
	src/optionWidget.h \
	GeneratedFiles/ui_optionWidget.h

# Specify any resources
RESOURCES += resource.qrc

INCLUDEPATH += GeneratedFiles

# Specify qt modules
QT += widgets