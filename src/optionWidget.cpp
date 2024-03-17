#include "optionWidget.h"

optionWidget::optionWidget(QWidget *parent, QString option)
	: QWidget(parent)
{
	ui.setupUi(this);
	ui.label->setText(option);
}
