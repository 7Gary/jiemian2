#ifndef ZZ_H
#define ZZ_H

#include <QWidget>

namespace Ui {
class zz;
}

class zz : public QWidget
{
    Q_OBJECT

public:
    explicit zz(QWidget *parent = nullptr);
    ~zz();

private:
    Ui::zz *ui;
};

#endif // ZZ_H
