#include "MCquestion.h"
#include "optionWidget.h"

MCquestion::MCquestion(QWidget *parent)
	: QWidget(parent)
{
	ui.setupUi(this);
	// initialize with dummy data
	ui.questionLabel->setText(tr("How many donkeys does it take to read the bible?"));
	QListWidgetItem *item = new QListWidgetItem(ui.listWidget); // create Listwidgetitem with listwidget as parent
	ui.listWidget->addItem(item); // add widget to listwidget
	optionWidget *optionWid = new optionWidget(nullptr, tr("32"));
	ui.listWidget->setItemWidget(item, optionWid);

	item = new QListWidgetItem(ui.listWidget);
	ui.listWidget->addItem(item);
	optionWid = new optionWidget(nullptr, tr("55"));
	ui.listWidget->setItemWidget(item, optionWid);
}
