#ifndef ZHIJIAN_H
#define ZHIJIAN_H

#include <QWidget>

namespace Ui {
class zhijian;
}

class zhijian : public QWidget
{
    Q_OBJECT

public:
    explicit zhijian(QWidget *parent = nullptr);
    ~zhijian();

private:
    Ui::zhijian *ui;
};

#endif // ZHIJIAN_H
