import flet
from flet import (
    Column,
    Container,
    Draggable,
    DragTarget,
    DragTargetAcceptEvent,
    Page,
    Row,
    border,
    Colors,
    ElevatedButton,
)

def main(page: Page):
    page.title = "Drag and Drop Color Mixing"

    # Змінні для збереження кольорів у першій та другій клітинці
    first_color = Colors.WHITE
    second_color = Colors.WHITE

    def drag_will_accept(e):
        # Встановлюємо колір обводки для клітинки на основі можливості прийняття
        e.control.content.border = border.all(
            2, Colors.BLACK45 if e.data == "true" else Colors.RED
        )
        e.control.update()

    def drag_accept(e: DragTargetAcceptEvent):
        nonlocal first_color, second_color
        
        # Отримуємо джерело перетягнутого елемента
        src = page.get_control(e.src_id)
        
        # Оновлюємо фон клітинки на колір джерела
        e.control.content.bgcolor = src.content.bgcolor
        e.control.content.border = None
        e.control.update()

        # Оновлюємо відповідний колір, залежно від того, яку клітинку змінили
        if e.control == first_color_target:
            first_color = src.content.bgcolor
        elif e.control == second_color_target:
            second_color = src.content.bgcolor

    def drag_leave(e):
        # Відновлюємо обводку клітинки, коли перетягування завершено
        e.control.content.border = None
        e.control.update()

    def reset_colors(e):
        # Скидаємо кольори у правих клітинках
        first_color_target.content.bgcolor = Colors.WHITE
        second_color_target.content.bgcolor = Colors.WHITE
        mix_target.content.bgcolor = Colors.BLUE_GREY_100
        first_color_target.update()
        second_color_target.update()
        mix_target.update()

        # Скидаємо значення кольорів
        nonlocal first_color, second_color
        first_color = Colors.WHITE
        second_color = Colors.WHITE

    def mix_colors_button(e):
        nonlocal first_color, second_color

        # Якщо обидва кольори не білий, змішуємо їх
        if first_color != Colors.WHITE and second_color != Colors.WHITE:
            mix_color = mix_colors(first_color, second_color)
            mix_target.content.bgcolor = mix_color  # Встановлюємо отриманий колір
            mix_target.update()

    # Словник для мапінгу кольорів з enum в їх назви
    color_map = {
        Colors.RED: 'red',
        Colors.GREEN: 'green',
        Colors.BLUE: 'blue',
        Colors.YELLOW: 'yellow',
    }

    def rgb_to_hex(r, g, b):
        # Перетворення RGB в HEX формат
        return f"#{r:02x}{g:02x}{b:02x}"

    def mix_colors(color1, color2):
        # Отримуємо імена кольорів
        color1_name = color_map.get(color1)
        color2_name = color_map.get(color2)

        # Спеціальний випадок для змішування синього та жовтого
        if {color1_name, color2_name} == {'blue', 'yellow'}:
            return Colors.GREEN  # Повертаємо зелений колір для синього і жовтого

        # Якщо кольори однакові, повертаємо початковий колір
        if color1_name == color2_name:
            return color1

        # Визначаємо RGB значення для кожного кольору
        rgb_map = {
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
        }

        r1, g1, b1 = rgb_map[color1_name]
        r2, g2, b2 = rgb_map[color2_name]

        # Змішуємо кольори, обчислюючи середнє значення RGB
        r = (r1 + r2) // 2
        g = (g1 + g2) // 2
        b = (b1 + b2) // 2

        # Перетворюємо результат в HEX
        return rgb_to_hex(r, g, b)

    # Мішень для змішування кольорів
    mix_target = DragTarget(
        group="color",
        content=Container(
            width=100,
            height=100,
            bgcolor=Colors.BLUE_GREY_100,  # Початковий колір
            border_radius=5,
        ),
        on_will_accept=drag_will_accept,
        on_accept=drag_accept,
        on_leave=drag_leave,
    )

    # Мішень для першого кольору
    first_color_target = DragTarget(
        group="color",
        content=Container(
            width=100,
            height=100,
            bgcolor=Colors.WHITE,  # Спочатку порожня клітинка
            border_radius=5,
        ),
        on_will_accept=drag_will_accept,
        on_accept=drag_accept,
        on_leave=drag_leave,
    )

    # Мішень для другого кольору
    second_color_target = DragTarget(
        group="color",
        content=Container(
            width=100,
            height=100,
            bgcolor=Colors.WHITE,  # Спочатку порожня клітинка
            border_radius=5,
        ),
        on_will_accept=drag_will_accept,
        on_accept=drag_accept,
        on_leave=drag_leave,
    )

    # Додаємо елементи на сторінку
    page.add(
        Row(
            [
                Column(
                    [
                        # Джерела для перетягування кольорів
                        Draggable(
                            group="color",
                            content=Container(
                                width=100,
                                height=100,
                                bgcolor=Colors.RED,  # Червоний колір
                                border_radius=5,
                            ),
                            content_feedback=Container(
                                width=20,
                                height=20,
                                bgcolor=Colors.RED,  # Червоний колір
                                border_radius=3,
                            ),
                        ),
                        Draggable(
                            group="color",
                            content=Container(
                                width=100,
                                height=100,
                                bgcolor=Colors.GREEN,  # Зелений колір
                                border_radius=5,
                            ),
                        ),
                        Draggable(
                            group="color",
                            content=Container(
                                width=100,
                                height=100,
                                bgcolor=Colors.BLUE,  # Синій колір
                                border_radius=5,
                            ),
                        ),
                        Draggable(
                            group="color",
                            content=Container(
                                width=100,
                                height=100,
                                bgcolor=Colors.YELLOW,  # Жовтий колір
                                border_radius=5,
                            ),
                        ),
                    ]
                ),
                Container(width=50),
                Column(
                    [
                        first_color_target,  # Мішень для першого кольору
                        second_color_target,  # Мішень для другого кольору
                        mix_target,  # Мішень для змішаного кольору
                        ElevatedButton(
                            text="Mix Colors",  # Кнопка для змішування кольорів
                            on_click=mix_colors_button,
                            bgcolor=Colors.GREEN,
                            width=150,
                        ),
                        ElevatedButton(
                            text="Reset",  # Кнопка для скидання кольорів
                            on_click=reset_colors,
                            bgcolor=Colors.RED,
                            width=150,
                        ),
                    ]
                ),
            ]
        )
    )

flet.app(main)
