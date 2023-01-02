import datetime
import matplotlib.pyplot as plt
import threading
import numpy as np
import logging

import pytz


logging.getLogger().setLevel(logging.INFO)
# change to DEBUG to print debug logs


class Clock:
    def __init__(self, period):
        self.timer = None
        self.period = period  # in seconds but can be float < 1.0

    def start(self):
        logging.debug('enter start')
        self.tick()
        # moving tick() before start maybe slows down the CPU usage
        self.timer = threading.Timer(self.period, self.start)
        # once we do timer.start(), after period seconds run target
        # function self.start, but since we are inside start() this
        # will be done forever or until we run stop()
        self.timer.start()
        logging.debug('leave start')

    def tick(self):
        self.datetime = datetime.datetime.now()
        # with attributes year, month, day, hour, minute, second, microsecond
        logging.debug(self.datetime)


# from https://python.plainenglish.io/building-an-analog-clock-using-python-518922d57784
# also https://gist.github.com/Kopfgeldjaeger/45b4cb02c48921a8ab238754c1034647#file-dynamic_clock
class AnalogClock:
    def __init__(self, timezone):
        self.timezone = timezone
        self._draw_clock()

    def _draw_clock(self):
        self.fig = plt.figure(figsize=(2.7, 2.5), dpi=100)
        self.ax = self.fig.add_subplot(111, polar=True)
        plt.cla()
        plt.setp(self.ax.get_yticklabels(), visible=False)
        self.ax.set_xticks(np.linspace(0, 2 * np.pi, 12, endpoint=False))
        self.ax.set_xticklabels(range(1, 13))
        self.ax.set_theta_direction(-1)
        self.ax.set_theta_offset(np.pi / 3.0)
        self.ax.grid(False)
        plt.ylim(0, 1)
        name_tz = self.timezone.zone.replace('_', ' ').replace('/', '\n')
        self.ax.text(3.2, 0.7, name_tz)  # like 'America/Argentina/Jujuy'
        plt.show(block=False)
        self._last_time = None
        # if new time - last time >= 1 sec, draw the time

    def _draw_time(self, the_time):
        hour = the_time.hour
        minute = the_time.minute
        second = the_time.second
        angles_h = 2 * np.pi * hour / 12 \
                   + 2 * np.pi * minute / (12 * 60) \
                   + 2 * second / (12 * 60 * 60) \
                   - np.pi / 6.0
        angles_m = 2 * np.pi * minute / 60 \
                   + 2 * np.pi * second / (60 * 60) \
                   - np.pi / 6.0
        angles_s = 2 * np.pi * second / 60 \
                   - np.pi / 6.0
        for line in self.ax.get_lines():
            line.remove()
        self.ax.plot([angles_s, angles_s], [0, 0.9], color="black", linewidth=1)
        self.ax.plot([angles_m, angles_m], [0, 0.7], color="black", linewidth=2)
        self.ax.plot([angles_h, angles_h], [0, 0.3], color="black", linewidth=4)
        self.fig.canvas.draw_idle()


class DigitalClock:
    def __init__(self, timezone):
        self.timezone = timezone
        self._draw_clock()

    def _draw_clock(self):
        self.handler = plt.figure(figsize=(3, 1.5))
        plt.axis('off')
        plt.axis('tight')
        self._first_time = True
        # if first time, draw the time

    def _draw_time(self, the_time):
        self.handler.clear()
        self.handler.text(0.5,0.5, '{:0>2}:{:0>2}'
                 .format(the_time.hour,
                         the_time.minute),
                 fontsize=48, ha='center', va='center')
        name_tz = self.timezone.zone.replace('_', ' ')
        self.handler.text(0.5, 0.2, name_tz, fontsize=20, ha='center',
                          va='center')
        self.handler.canvas.draw_idle()
        self.handler.show()


if __name__ == '__main__':
    clock = Clock(1.0)
    clock.start()

    num_clocks = 3
    timezones = np.random.choice(pytz.common_timezones, num_clocks, replace=False)
    print(timezones)

    analog_clocks = []
    digital_clocks = []
    for i in range(num_clocks):
        tz = pytz.timezone(timezones[i])
        analog = AnalogClock(tz)
        digital = DigitalClock(tz)
        analog_clocks.append(analog)
        digital_clocks.append(digital)
        dt = datetime.datetime.now() # local date time
        analog._draw_time(dt.astimezone(tz)) # localized date time
        digital._draw_time(dt.astimezone(tz))

    def stop_last_analog_clock():
        pass #TODO

    threading.Timer(10.0, stop_last_analog_clock).start()
    # after 10 seconds stop the last analog clock