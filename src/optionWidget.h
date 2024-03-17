#include <QtWidgets/QWidget>
#include "ui_optionWidget.h"

class optionWidget : public QWidget
{
	Q_OBJECT
private:

public:
	optionWidget(QWidget *parent = Q_NULLPTR, QString option = tr("[REDACTED]"));

private:
	Ui::optionWidgetClass ui;
};
