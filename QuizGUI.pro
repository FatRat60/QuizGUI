#Specify target exec name
TARGET = QuizGUI

# Specify source
SOURCES += \
    src/main.cpp \
	src/MCquestion.cpp

# Specify any headers
HEADERS += \
	src/MCquestion.h

# Specify any resources
RESOURCES += resource.qrc

# Specify qt modules
QT += widgets