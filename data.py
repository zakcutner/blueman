from models import Question, Statement

questions = {
    'road': Question(id='road',
                     text='On a <strong>road</strong>?',
                     image='road.png'),

    'single': Question(id='single',
                       text='On a <strong>single yellow line</strong>?',
                       image='single_yellow.png'),

    'double': Question(id='double',
                       text='On a <strong>double yellow line</strong>?',
                       image='double_yellow.png'),

    'single_or_double': Question(id='single_or_double',
                                 text='On <strong>single</strong> or <strong>double yellow lines</strong>?',
                                 image='yellow_lines.png'),

    'single_or_double_2': Question(id='single_or_double_2',
                                   text='On <strong>single</strong> or <strong>double yellow lines</strong>?',
                                   image='yellow_lines.png'),

    'disabled_bay': Question(id='disabled_bay',
                             text='In a <strong>disabled bay</strong>?'),

    'meters': Question(id='meters',
                       text='At a <strong>parking meter</strong>?',
                       image='meters.png'),

    'pay_and_display': Question(id='pay_and_display',
                                text='In a <strong>pay and display bay</strong>?',
                                image='pay_and_display.png'),

    'resident': Question(id='resident',
                         text='In a <strong>resident bay</strong>?'),

    'pay_and_display_or_resident': Question(id='pay_and_display_or_resident',
        text='In a <strong>resident bay</strong> or <strong>pay and display bay</strong>?',
        image='pay_and_display.png'),

    'blue_badge': Question(id='blue_badge',
                           text='With a <strong>Blue Badge</strong> holder?',
                           image='blue_badge.png'),

    'red_badge': Question(id='red_badge',
                          text='With a disabled <strong>Red Badge</strong> holder?'),

    'purple_badge': Question(id='purple_badge',
                             text='With a <strong>Purple Badge</strong> holder?'),

    'white_badge': Question(id='white_badge',
                            text='With a disabled <strong>White Badge</strong>?'),

    'green_badge': Question(id='green_badge',
                            text='With a disabled <strong>Green Badge</strong>?'),

}

statements = {
    'carpark': Statement(id='carpark',
                         text='Check <strong>local signage</strong> for more information!'),

    'unlimited': Statement(id='unlimited',
                           text='For <strong>free</strong>, with <stnog>no time limit</strong> unless signposted.'),

    '20minutes_dropoff': Statement(id='20minutes_dropoff',
                                   text='For <strong>20 minutes</strong>, to <strong>pick up or drop off</strong> a <strong>disabled person</strong>.'),

    '30minutes': Statement(id='30minutes',
                           text='For up to <strong>30 minutes</strong>.'),

    '4hours': Statement(id='4hours',
                        text='For up to <strong>4 hours</strong> in <strong>controlled time</strong>, otherwise <strong>unlimited</strong>.'),

    '3hours': Statement(id='3hours',
                        text='For up to <strong>3 hours</strong> at a time, leaving <strong>1 hour in between</strong>.'),

    'weekdaylimit': Statement(id='weekdaylimit',
                              text='For <strong>free</strong>, but only for <strong>four hours on weekdays</strong>.'),

    'none': Statement(id='none',
                      text='Only if <strong>normal restrictions</strong> allow you to.'),

    'normalfeewithextension': Statement(id='payanddisplay',
                                        text='If you pay the <strong>normal fee</strong>, but you can stay for an <strong>extra hour</strong>.'),

    'uncontrolledhours': Statement(id='uncontrolledhours',
                                   text='For <strong>free</strong> in <strong>uncontrolled hours</strong>.')
}

steps = {
    'City of London': {
        'blue_badge': ['road', 'none'],
        'road': ['red_badge', 'carpark'],

        'red_badge': ['single', 'disabled_bay'],

        'single': ['30minutes', 'pay_and_display'],

        'disabled_bay': ['weekdaylimit', 'single_or_double'],
        'single_or_double': ['none, pay_and_display'],

        'pay_and_display': ['normalfeewithextension', 'none'],
    },

    'Kensington and Chelsea': {
        'blue_badge': ['road', 'none'],
        'road': ['purple_badge', 'carpark'],
        'purple_badge': ['single_or_double', 'single_or_double_2'],

        'single_or_double': ['20minutes_dropoff', 'pay_and_display_or_resident'],
        'pay_and_display_or_resident': ['unlimited', 'none'],

        'single_or_double_2': ['none, pay_and_display'],
        'pay_and_display': ['normalfeewithextension', 'none'],
    },

    'Westminster': {
        'blue_badge': ['road', 'none'],
        'road': ['single_or_double', 'carpark'],
        'single_or_double': ['uncontrolledhours', 'double'],
        'double': ['none', 'disabled_bay'],
        'disabled_bay': ['4hours', 'white_badge'],
        'white_badge': ['pay_and_display_or_resident', 'resident'],
        'pay_and_display_or_resident': ['unlimited', 'none'],
        'resident': ['uncontrolledhours', 'pay_and_display'],
        'pay_and_display': ['normalfeewithextension', 'none'],
    },

    'Camden': {
        'blue_badge': ['road', 'none'],
        'road': ['disabled_bay', 'carpark'],
        'disabled_bay': ['unlimited', 'green_badge'],
        'green_badge': ['pay_and_display_or_resident', 'none'],
        'pay_and_display_or_resident': ['unlimited', 'none'],
    },

    '*': {
        'blue_badge': ['road', 'none'],
        'road': ['single_or_double', 'carpark'],
        'single_or_double': ['3hours', 'disabled_bay'],
        'disabled_bay': ['unlimited', 'meters'],
        'meters': ['unlimited', 'none'],
    },
}
