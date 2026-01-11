#include "peifang.h"
#include "add.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    add w;
    w.show();
    return a.exec();
}
