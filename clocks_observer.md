---
marp: true
paginate: true
---

Observer in Python
===

![bg right width:600 ](observer_refactoring_guru.png)
image from [http://refactoring.guru](http://refactoring.guru)

---

Exercise
===

- Implement in Python classes *analogous* to Java's ```java.util.Observer``` interface and ```java.util.Observable``` abstract class.

- *analogous* = equivalent functionality, not literal translation, for instance no need of ```hasChanged(), setChanged()```

- Apply them to show the time at several world time zones

---

![bg](clocks.png)

---

*Observer* in ```java.util```
===

![height:350](observer_java.png)

- ``Observable`` is an abstract class with all these methods implemented
- An ``Observable`` keeps a list of its observers (composition not shown here)
- concrete observables inherit them and don't override them
- ``update()`` is abstract and has to be implemented by concrete observers

---

``Clock.py``
===

```python
class Clock:
    def __init__(self, period):
        self.timer = None
        self.period = period  # in seconds but can be float < 1.0

    def start(self):
        self.tick()
        # moving tick() before start maybe slows down the CPU usage
        self.timer = threading.Timer(self.period, self.start)
        # once we do timer.start(), after period seconds run target
        # function self.start, but since we are inside start() this
        # will be done forever or until we run stop()
        self.timer.start()

    def tick(self):
        self.datetime = datetime.datetime.now()
        # with attributes year, month, day, hour, minute, second, microsecond
        logging.debug(self.datetime)
```

---

``AnalogClock``
===

```python
class AnalogClock:
    def __init__(self, timezone):
        self.timezone = timezone
        self._draw_clock()

    def _draw_clock(self):
        self.fig = plt.figure(figsize=(2.7, 2.5), dpi=100)
        # ...
        # sentences to draw an analog clock = circle + numbers 1..12 + text time zone
        self._last_time = None
        # if new time - last time >= 1 sec, draw the time

    def _draw_time(self, the_time):
        hour = the_time.hour
        minute = the_time.minute
        second = the_time.second
        angles_h = 2 * np.pi * hour / 12 + 2 * np.pi * minute / (12 * 60) \
                   + 2 * second / (12 * 60 * 60) - np.pi / 6.0
        angles_m = 2 * np.pi * minute / 60 + 2 * np.pi * second / (60 * 60) \
                   - np.pi / 6.0
        angles_s = 2 * np.pi * second / 60 - np.pi / 6.0
        for line in self.ax.get_lines(): line.remove()
        self.ax.plot([angles_s, angles_s], [0, 0.9], color="black", linewidth=1)
        self.ax.plot([angles_m, angles_m], [0, 0.7], color="black", linewidth=2)
        self.ax.plot([angles_h, angles_h], [0, 0.3], color="black", linewidth=4)
        self.fig.canvas.draw_idle()
```

---

``DigitalClock``
===

```python
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
```

---

``clocks.py``
===


```python
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
        #
        # TODO: change the following lines
        #
        dt = datetime.datetime.now() # local date time
        analog._draw_time(dt.astimezone(tz)) # localized date time
        digital._draw_time(dt.astimezone(tz))

    def stop_last_analog_clock():
        pass #TODO

    threading.Timer(10.0, stop_last_analog_clock).start()
    # after 10 seconds stop the last analog clock
```

--- 

The code we are giving you paints these **static** clocks:

![width:900](clocks_students.png)

---


```python
if __name__ == '__main__':
    #...

    def stop_last_analog_clock():
        pass #TODO

    threading.Timer(10.0, stop_last_analog_clock).start()
    # after 10 seconds stop the last analog clock
```

In your implementation you have to stop the last created analog clock after 10 seconds starting all the clocks. 

What does it mean to stop a desktop clock ? To stop updating it.

---
Note that rightmost analog clock as a different seconds time because I've stopped it.

![width:900](clocks.png)

---


---

Deliverables
===

- Python source code
- detailed PlantUML class diagram, with concrete observers and observables
- printscreens to show it works

