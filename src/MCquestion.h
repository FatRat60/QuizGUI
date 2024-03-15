#include <QtWidgets/QWidget>
#include "ui_MCquestion.h"

class MCquestion : public QWidget
{
	Q_OBJECT
private:

public:
	MCquestion(QWidget *parent = Q_NULLPTR);
	void initialize();

private:
	Ui::MCQuestionClass ui;
};
