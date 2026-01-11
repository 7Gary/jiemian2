#include "zz.h"
#include "ui_zz.h"

zz::zz(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::zz)
{
    ui->setupUi(this);
}

zz::~zz()
{
    delete ui;
}
