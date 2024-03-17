#include <QtWidgets/QApplication>
#include "MCquestion.h"

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);
    MCquestion w;
    w.show();
    return app.exec();
}