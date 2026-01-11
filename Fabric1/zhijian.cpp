#include "zhijian.h"
#include "ui_zhijian.h"

zhijian::zhijian(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::zhijian)
{
    ui->setupUi(this);
}

zhijian::~zhijian()
{
    delete ui;
}
