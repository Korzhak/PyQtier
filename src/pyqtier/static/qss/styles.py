NOTIFICATION_STYLES = {
    'success': """
        QLabel {
            background-color: rgba(76, 175, 80, 220);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid rgba(76, 175, 80, 255);
        }
    """,
    'error': """
        QLabel {
            background-color: rgba(244, 67, 54, 220);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid rgba(244, 67, 54, 255);
        }
    """,
    'warning': """
        QLabel {
            background-color: rgba(255, 152, 0, 220);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid rgba(255, 152, 0, 255);
        }
    """,
    'info': """
        QLabel {
            background-color: rgba(33, 150, 243, 220);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid rgba(33, 150, 243, 255);
        }
    """,
}

DOCK_DARK_STYLE = """
    /* Кнопка закриття на вкладці (приховано) */
    ads--CDockWidgetTab > QPushButton { max-width: 0; max-height: 0; padding: 0; margin: 0; border: none; }

    /* Заголовок області доків (верхня панель з вкладками) */
    ads--CDockAreaTitleBar { background: rgb(40,40,40); min-height: 15px; max-height: 15px; }

    /* Кнопки в заголовку (закрити, меню) */
    ads--CDockAreaTitleBar QAbstractButton { background: rgb(40,40,40); border: none; }

    /* Текст неактивної вкладки */
    ads--CDockWidgetTab QLabel { background: rgb(40,40,40); color: rgb(100,100,100); }

    /* Фон вкладки */
    ads--CDockWidgetTab { background: rgb(40,40,40); }

    /* Текст активної вкладки */
    ads--CDockWidgetTab[activeTab="true"] QLabel { color: white; }

    /* Рамка навколо області доку */
    ads--CDockAreaWidget { border: 1px solid rgb(40,40,40); border-radius: 4px; }

    /* Контейнер вмісту доку */
    ads--CDockWidget > QScrollArea { border: none; }
"""

DOCK_LIGHT_STYLE = """
    /* Кнопка закриття на вкладці (приховано) */
    ads--CDockWidgetTab > QPushButton { max-width: 0; max-height: 0; padding: 0; margin: 0; border: none; }

    /* Заголовок області доків */
    ads--CDockAreaTitleBar { background: rgb(240,240,240); min-height: 15px; max-height: 15px; }

    /* Кнопки в заголовку */
    ads--CDockAreaTitleBar QAbstractButton { background: rgb(240,240,240); border: none; }

    /* Текст неактивної вкладки */
    ads--CDockWidgetTab QLabel { background: rgb(240,240,240); color: rgb(100,100,100); }

    /* Фон вкладки */
    ads--CDockWidgetTab { background: rgb(240,240,240); }

    /* Текст активної вкладки */
    ads--CDockWidgetTab[activeTab="true"] QLabel { color: black; }

    /* Рамка навколо області доку */
    ads--CDockAreaWidget { border: 1px solid rgb(200,200,200); border-radius: 4px; }

    /* Контейнер вмісту доку */
    ads--CDockWidget > QScrollArea { border: none; }
"""
