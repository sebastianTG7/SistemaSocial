Flet automatically calls page.update() (or .update() on the nearest isolated ancestor) at the end of every event handler and main() function. This means you don't need to call .update() yourself in most cases:


import flet as ft


def main(page: ft.Page):
    def button_click(e):
        page.controls.append(ft.Text("Clicked!"))
        # no need to call page.update() — it happens automatically

    page.controls.append(ft.Button("Click me", on_click=button_click))
    # no need to call page.update() here either


ft.run(main)
Note

If your event handler already calls .update() explicitly (e.g. code written for Flet 0.x), the automatic update is skipped to avoid a redundant double update.

Disabling auto-update#
You can disable auto-update for fine-grained control over when updates are sent to the client. Use ft.context.disable_auto_update() and ft.context.enable_auto_update() to toggle the behavior.

When called inside a handler, the setting applies to the current handler context only:


import flet as ft


def main(page: ft.Page):
    def add_many_items(e):
        ft.context.disable_auto_update()
        for i in range(100):
            page.controls.append(ft.Text(f"Item {i}"))
        page.update()  # single update for all 100 items

    page.controls.append(ft.Button("Add items", on_click=add_many_items))


ft.run(main)
When called outside of event handlers (e.g. at the module level), it controls the global default for the entire app:


import flet as ft

# disable auto-update globally
ft.context.disable_auto_update()


def main(page: ft.Page):
    def button_click(e):
        page.controls.append(ft.Text("Clicked!"))
        page.update()  # must call explicitly since auto-update is off

    page.controls.append(ft.Button("Click me", on_click=button_click))
    page.update()


ft.run(main)
Now let's see Flet in action by running the app!
Running a Flet app (Hot Reload)
Flet apps can be executed as either desktop or web applications using the flet run command. Doing so will start the app in a native OS window or a web browser, respectively, with hot reload enabled to view changes in real-time.

Desktop app#
To run Flet app as a desktop app, use the following command:


uv
pip

flet run

When you run the command without any arguments, main.py script in the current directory will be executed, by default.

If you need to provide a different path, use the following command:


uv
pip

flet run [script]

Where [script] is a relative (ex: counter.py) or absolute (ex: /Users/john/projects/flet-app/main.py) path to the Python script you want to run.

The app will be started in a native OS window:

macOS

macOS

Windows

windows

Web app#
To run Flet app as a web app, use the --web (or -w) option:


uv
pip

flet run --web [script]  

A new browser window/tab will be opened and the app will be using a random TCP port:

Web

Running Flet app as a web app

Watching for changes#
By default, Flet will watch the script file that was run and reload the app whenever the contents of this file are modified+saved, but will not watch for changes in other files.

To modify this behavior, you can use one or more of these flet run options:

-d or --directory to watch for changes in the [script]s directory only
-r or --recursive to watch for changes in the [script]s directory and all sub-directories recursively
Example


uv
pip

flet run --recursive [script]

ToDo
In this tutorial we will show you, step-by-step, how to create a To-Do app in Python using Flet framework and then publish it as a desktop, mobile or web app. The app is a single-file console program of just 163 lines (formatted!) of Python code, yet it is a multi-platform application with rich, responsive UI:

complete-demo-web.gif

You can see the live demo here.

We chose a To-Do app for the tutorial, because it covers all of the basic concepts you would need to create a Flet app: building a page layout, adding controls, handling events, displaying and editing lists, making reusable UI components, and publishing options.

The tutorial consists of the following steps:

Getting started with Flet
Adding page controls and handling events
View, edit and delete list items
Filtering list items
Final touches
Publishing the app
Getting started with Flet#
To create a multi-platform app in Python with Flet, you don't need to know HTML, CSS or JavaScript, but you do need a basic knowledge of Python and object-oriented programming.

Before you can create your first Flet app, you need to setup your development environment, which requires Python 3.10 or above and flet package.

Once you have Flet installed, let's create a simple hello-world app.

Create hello.py with the following contents:

hello.py

import flet as ft


def main(page: ft.Page):
    page.add(ft.Text(value="Hello, world!"))


ft.run(main)
Run this app and you will see a new window with a greeting:

hello-world.png

Adding page controls and handling events#
To start, we'll need a TextField for entering a task name, and "+" FloatingActionButton with an event handler that will display a Checkbox with a new task.

Create todo.py with the following contents:

todo.py

import flet
from flet import Checkbox, FloatingActionButton, Icons, Page, TextField


def main(page: Page):
    def add_clicked(e):
        page.add(Checkbox(label=new_task.value))
        new_task.value = ""
        page.update()

    new_task = TextField(hint_text="Whats needs to be done?")

    page.add(new_task, FloatingActionButton(icon=Icons.ADD, on_click=add_clicked))


flet.run(main)
Run the app and you should see a page like this:

app-1.png

Page layout#
Now let's make the app look nice! We want the entire app to be at the top center of the page, taking up 600 px width. The TextField and the "+" button should be aligned horizontally, and take up full app width:

diagram-1.svg

Row is a control that is used to lay its children controls out horizontally on a page. Column is a control that is used to lay its children controls out vertically on a page.

Replace todo.py contents with the following:

hello.py

import flet as ft


def main(page: ft.Page):
    def add_clicked(e):
        tasks_view.controls.append(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        view.update()

    new_task = ft.TextField(hint_text="What needs to be done?", expand=True)
    tasks_view = ft.Column()
    view = ft.Column(
        width=600,
        controls=[
            ft.Row(
                controls=[
                    new_task,
                    ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_clicked),
                ],
            ),
            tasks_view,
        ],
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(view)


ft.run(main)
Run the app and you should see a page like this:

app-2.png

Reusable UI components#
While we could continue writing our app in the main function, the best practice would be to create a reusable UI component. Imagine you are working on an app header, a side menu, or UI that will be a part of a larger project. Even if you can't think of such uses right now, we still recommend creating all your Flet apps with composability and reusability in mind.

To make a reusable To-Do app component, we are going to encapsulate its state and presentation logic in a separate class:

todo.py

import flet as ft


@ft.control
class TodoApp(ft.Column):
    # application's root control is a Column containing all other controls
    def init(self):
        self.new_task = ft.TextField(hint_text="What needs to be done?", expand=True)
        self.tasks_view = ft.Column()
        self.width = 600
        self.controls = [
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, on_click=self.add_clicked
                    ),
                ],
            ),
            self.tasks_view,
        ]

    def add_clicked(self, e):
        self.tasks_view.controls.append(ft.Checkbox(label=self.new_task.value))
        self.new_task.value = ""
        self.update()


def main(page: ft.Page):
    page.title = "To-Do App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # create application instance
    todo = TodoApp()

    # add application's root control to the page
    page.add(todo)


ft.run(main)
Try this out!
View, edit and delete list items#
In the previous step, we created a basic To-Do app with task items shown as checkboxes. Let's improve the app by adding "Edit" and "Delete" buttons next to a task name. The "Edit" button will switch a task item to edit mode.

diagram-2.svg

Each task item is represented by two rows: display_view row with Checkbox, "Edit" and "Delete" buttons and edit_view row with TextField and "Save" button. view column serves as a container for both display_view and edit_view rows.

To encapsulate task item views and actions, we introduced a new Task class.

Additionally, we changed TodoApp class to create and hold Task instances when the "Add" button is clicked.

For "Delete" task operation, we implemented task_delete() method in TodoApp class which accepts task control instance as a parameter.

Then, we passed a reference to task_delete method into Task constructor and called it on "Delete" button event handler.

todo.py

from dataclasses import field
from typing import Callable

import flet as ft


@ft.control
class Task(ft.Column):
    task_name: str = ""
    on_task_delete: Callable[["Task"], None] = field(default=lambda task: None)

    def init(self):
        self.display_task = ft.Checkbox(value=False, label=self.task_name)
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.on_task_delete(self)


@ft.control
class TodoApp(ft.Column):
    # application's root control is a Column containing all other controls
    def init(self):
        self.new_task = ft.TextField(hint_text="What needs to be done?", expand=True)
        self.tasks = ft.Column()
        self.width = 600
        self.controls = [
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, on_click=self.add_clicked
                    ),
                ],
            ),
            self.tasks,
        ]

    def add_clicked(self, e):
        task = Task(task_name=self.new_task.value, on_task_delete=self.task_delete)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()


def main(page: ft.Page):
    page.title = "To-Do App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # create application instance
    app = TodoApp()

    # add application's root control to the page
    page.add(app)


ft.run(main)
Run the app and try to edit and delete tasks:

view-edit-delete.gif

Filtering list items#
We already have a functional To-Do app where we can create, edit, and delete tasks. To be even more productive, we want to be able to filter tasks by their status.

Copy the entire code for this step from here. Below we will explain the changes we've done to implement filtering.

Tabs control is used to display filter:

todo.py

# ...

class TodoApp(ft.Column):
    # application's root control is a Column containing all other controls
    def init(self):
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = ft.Column()

        self.filter = ft.TabBar(
            scrollable=False,
            tabs=[
                ft.Tab(label="all"),
                ft.Tab(label="active"),
                ft.Tab(label="completed"),
            ],
        )

        self.filter_tabs = ft.Tabs(
            length=3,
            selected_index=0,
            on_change=lambda e: self.update(),
            content=self.filter,
        )

    # ...
To display different lists of tasks depending on their statuses, we could maintain three lists with "All", "Active" and "Completed" tasks. We, however, chose an easier approach where we maintain the same list and only change a task's visibility depending on its status.

In TodoApp class we overrode before_update() method called every time when the control is being updated. It iterates through all the tasks and updates their visible property depending on the status of the task:

todo.py

class TodoApp(ft.Column):

    # ...

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and task.completed == False)
                or (status == "completed" and task.completed)
            )
Filtering should occur when we click on a tab or change a task status. TodoApp.before_update() method is called when Tabs selected value is changed or Task item checkbox is clicked:

todo.py

class TodoApp(ft.Column):

    # ...

    def tabs_changed(self, e):
        self.update()

    def task_status_change(self, e):
        self.update()


    def add_clicked(self, e):
        task = Task(
            task_name=self.new_task.value,
            on_status_change=self.task_status_change,
            on_delete=self.task_delete,
        )
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()
    # ...

class Task(ft.Column):
    task_name: str = ""
    on_status_change: Callable[[], None] = field(default=lambda: None)
    on_delete: Callable[["Task"], None] = field(default=lambda task: None)

    # ...

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change()
Run the app and try filtering tasks by clicking on the tabs:

filtering.gif

Final touches#
Our Todo app is almost complete now. As a final touch, we will add a footer (Column control) displaying the number of incomplete tasks (Text control) and a "Clear completed" button.

Full code
app-4

Publishing the app#
Congratulations! You have created your first Python app with Flet, and it looks awesome!

Now it's time to share your app with the world!

Follow these instructions to publish your Flet app as a mobile, desktop or web app.

Summary#
In this tutorial, you have learnt how to:

Create a simple Flet app;
Work with Reusable UI components;
Design UI layout using Column and Row controls;
Work with lists: view, edit and delete items, filtering;
Publish your Flet app to multiple platforms;
For further reading you can explore controls and examples.
Windows
Instructions for packaging a Flet app into a Windows application.

Info

This guide provides detailed Windows-specific information. Complementary and more general information is available here.

Prerequisites#
Visual Studio#
Visual Studio (2022 or 2026) is required with the Desktop development with C++ workload installed.

Follow this guide for instructions on downloading and installing correct Visual Studio components for Flutter desktop development.

flet build windows#
Note

This command can be run on Windows only.

Builds a Windows application.

Troubleshooting#
Developer mode#
If you get the below error:


Building with plugins requires symlink support.

Please enable Developer Mode in your system settings. Run
  start ms-settings:developers
to open settings.


Creating an Extension
While Flet controls leverage many built-in Flutter widgets to enable the creation of complex applications, not all Flutter widgets or third-party packages can be directly supported by the Flet team or included in the core Flet framework. At the same time, the Flutter ecosystem is vast and offers developers a wide range of possibilities to extend functionality beyond the core.

To address this, the Flet framework provides an extensibility mechanism. This allows you to incorporate widgets and APIs from your own custom Flutter packages or third-party libraries directly into your Flet application.

In this guide, you will learn how to create Flet extension from template and then customize it to integrate 3rd-party Flutter package into your Flet app.

Prerequisites#
To integrate custom Flutter package into Flet you need to have basic understanding of how to create Flutter apps and packages in Dart language and have Flutter development environment configured. See Flutter Getting Started for more information about Flutter and Dart.

Create Flet extension from template#
Flet now makes it easy to create and build projects with your custom controls based on Flutter widgets or Flutter 3rd-party packages. In the example below, we will be creating a custom Flet extension based on the flutter_spinkit package.

Step 1. Create new virtual environment and install Flet there.

Step 2. Create new extension project from template.


flet create --template extension --project-name flet-spinkit
A project with new FletSpinkit control will be created. The control is just a Flutter Text widget with text property, which we will customize later.

Step 3. Build example app.

Flet project created from extension template has examples/flet_spinkit_example folder with the example app.

When in the folder where your pyproject.toml for the app is (examples/flet_spinkit_example), run flet build command, for example, for macos:


flet build macos -v
Open the app and see the new custom Flet Control:


open build/macos/flet-spinkit-example.app


Change Python files#
Once the project was built for desktop once, you can make changes to your python files and run it without rebuilding.

First, if you are not using uv, install dependencies from pyproject.toml:


pip install .
or

poetry install
Now you can make changes to your example app main.py:


import flet as ft

from flet_spinkit import FletSpinkit


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Container(
            height=150,
            width=300,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.PINK_200,
            content=FletSpinkit(
                tooltip="My new PINK FletSpinkit Control tooltip",
                value="My new PINK FletSpinkit Flet Control",
            ),
        ),
    )


ft.run(main)
and run:


flet run


Change Flutter package#
When you make any changes to your flutter package, you need to rebuild:


flet build macos -v
If you need to debug, run this command:


build/macos/flet-spinkit-example.app/Contents/MacOS/flet-spinkit-example --debug
Integrate 3rd-party Flutter package#
Let's integrate flutter_spinkit package into our Flet app.

Step 1. Add dependency

Go to src/flutter/flet_spinkit folder and run this command to add dependency to flutter_spinkit to pubspec.yaml:


flutter pub add flutter_spinkit
Read more information about using Flutter packages here.

Step 2. Modify dart file

In the src/flutter/flet_spinkit/lib/src/flet_spinkit.dart file, add import statement and replace Text widget with SpinKitRotatingCircle widget:


import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class FletSpinkitControl extends StatelessWidget {
  final Control control;

  const FletSpinkitControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    Widget myControl = SpinKitRotatingCircle(color: Colors.red, size: 100.0);

    return LayoutControl(control: control, child: myControl);
  }
}
Step 3. Rebuild example app

Go to examples/flet_spinkit_example, clear cache and rebuild your app:


flet build macos -v
Step 4. Run your app



Flet extension structure#
After creating new Flet project from extension template, you will see the following folder structure:


├── LICENSE
├── mkdocs.yml
├── README.md
├── docs
│   └── index.md
│   └── FletSpinkit.md
├── examples
│   └── flet_spinkit_example
│       ├── README.md
│       ├── pyproject.toml
│       └── src
│           └── main.py
├── pyproject.toml
└── src
    ├── flet_spinkit
    │   ├── __init__.py
    │   └── flet_spinkit.py
    └── flutter
        └── flet_spinkit
            ├── CHANGELOG.md
            ├── LICENSE
            ├── README.md
            ├── lib
            │   ├── flet_spinkit.dart
            │   └── src
            │       ├── create_control.dart
            │       └── flet_spinkit.dart
            └── pubspec.yaml
Flet extension consists of: * package, located in src folder * example app, located in examples/flet-spinkit_example folder * docs, located in docs folder

Package#
Package is the component that will be used in your app. It consists of two parts: Python and Flutter.

Python#
flet_spinkit.py#
Defines the Python-side Flet control. FletSpinkit is registered with @ft.control("flet_spinkit") and inherits from ft.LayoutControl, which ties it to the Flutter Control.type handled in the extension. The class currently includes a value: str property and a placeholder docstring.

Flutter#
pubspec.yaml#
Flutter package manifest for the extension. Declares SDK constraints and dependencies. Notable deps:

flet for Flet extension APIs
flutter_spinkit for the spinner widgets used by the control
flet_spinkit.dart#
Library entrypoint. Exports the public Extension class from extension.dart.

src/extension.dart#
Registers the extension with Flet. Extension.createWidget maps Control.type to the Flutter widget; currently maps "flet_spinkit" to FletSpinkitControl.

src/flet_spinkit.dart#
Flutter wrapper widget for the control. FletSpinkitControl builds a SpinKitRotatingCircle and wraps it with LayoutControl so layout/state from the Python control are applied.

Example app#
src/main.py#
Python program that uses Flet Python control.

pyproject.toml#
Here you specify dependency to your package, which can be:

Path dependency
Absolute path to your Flet extension folder, for example:


dependencies = [
  "flet-spinkit @ file:///Users/user-name/projects/flet-spinkit",
  "flet>=0.80.2",
]
Git dependency
Link to git repository, for example:


dependencies = [
  "flet-ads @ git+https://github.com/flet-dev/flet-ads.git",
  "flet>=0.80.2",
]
PyPi dependency
Name of the package published on pypi.org, for example:


dependencies = [
  "flet-ads",
  "flet>=0.80.2",
]
Docs#
If you are planning to share your extension with community, you can easily generate documentation from your source code using mkdocs.

Flet extension comes with a docs folder containing initial files for your documentation and a mkdocs.yml file at the project root.

From the folder that contains mkdocs.yml, run the following command to see how your docs look locally:


mkdocs serve
Open http://127.0.0.1:8000 in your browser:



Once your documentation is ready, if your package is hosted on GitHub, your can run the following command to host your documentation on GitHub pages:


mkdocs gh-deploy
You may find this guide helpful to get started with mkdocs.

Customize properties#
In the example above, Spinkit control creates a hardcoded Flutter widget. Now let's customize its properties.

Common properties#
Generally, there are three types of controls in Flet:

Visual controls that are added to the app/page surface, such as FletSpinkit.

Dialog and other popup controls (dialogs, pickers, panels, etc.) that are opened from the page (for example, page.open(dlg)).

Services (Clipboard, Battery, Video, Audio, etc.) that are created as standalone instances and automatically registered with the page.

When creating a visual control that should participate in layout (size, position, transforms, margin, etc.), define a dataclass-based control annotated with @ft.control("control_name") and inherit from LayoutControl. In its Dart counterpart (src/flet_spinkit.dart), wrap your Flutter widget with LayoutControl(...).

When creating a dialog or other popup control (opened with page.open(...)), define a dataclass-based control annotated with @ft.control("control_name") and inherit from DialogControl. In its Dart counterpart, show the dialog/popup (for example, showDialog or showModalBottomSheet) and return a placeholder widget like SizedBox.shrink() instead of wrapping with LayoutControl(...) or BaseControl(...).

When creating a service control (Clipboard, Battery, Video, Audio, etc.), define a dataclass-based control annotated with @ft.control("control_name") and inherit from Service. In its Dart counterpart, implement FletService and register it via FletExtension.createService (no widget wrapper).

You can use all LayoutControl, DialogControl, and Service properties inherited by your dataclass-based control without re-declaring them as fields (unless you want to override defaults or metadata).

If you have created your extension project from Flet extension template, your Python Control is already inherited from LayoutControl and you can use its properties in your example app:


import flet as ft

from flet_spinkit import FletSpinkit


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Stack(
            [
                ft.Container(height=200, width=200, bgcolor=ft.Colors.BLUE_100),
                FletSpinkit(opacity=0.5, tooltip="Spinkit tooltip", top=0, left=0),
            ]
        )
    )


ft.run(main)


Control-specific properties#
Now that you have taken full advantage of the properties Flet LayoutControl offer, let's define the properties that are specific to the new Control you are building.

In the FletSpinkit example, let's define its color and size.

In Python class, define new color and size properties:


from typing import Optional

import flet as ft


@ft.control("flet_spinkit")
class FletSpinkit(ft.LayoutControl):
    """
    FletSpinkit Control description.
    """

    color: Optional[ft.ColorValue] = None
    size: float = 100.00
In src/flet_spinkit.dart file, use helper methods getColor and getDouble to access color and size values:


import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class FletSpinkitControl extends StatelessWidget {
  final Control control;

  const FletSpinkitControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    Widget myControl = SpinKitRotatingCircle(
      color: control.getColor("color", context),
      size: control.getDouble("size") ?? 100.0,
    );

    return LayoutControl(control: control, child: myControl);
  }
}
Use color and size properties in your app:


import flet as ft

from flet_spinkit import FletSpinkit


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Stack(
            controls=[
                ft.Container(height=200, width=200, bgcolor=ft.Colors.BLUE_100),
                FletSpinkit(
                    color=ft.Colors.YELLOW,
                    size=150,
                    opacity=0.5,
                    tooltip="Spinkit tooltip",
                    top=0,
                    left=0,
                ),
            ]
        )
    )


ft.run(main)
Rebuild and run:



Important: Default values must match on both sides

Properties with default values on the Python side are not sent to Flutter when the user hasn't changed them from the default. This means your Dart code must provide the same default value for every property that has one in Python.

For example, if your Python control declares:


size: float = 100.0
animate: bool = True
Then your Dart code must use matching defaults:


// Correct - defaults match Python
final size = control.getDouble("size", 100.0)!;
final animate = control.getBool("animate", true)!;

// Wrong - no default, will be null when user doesn't set the property
final size = control.getDouble("size");      // returns null!
final animate = control.getBool("animate");  // returns null!
This also applies to @ft.value types parsed with helper functions. If a value type field has a default, the corresponding parseDouble(), parseBool(), parseDuration(), etc. call on the Dart side must provide the same default.

Common pitfalls:

Missing defaults: control.getDouble("prop") instead of control.getDouble("prop", 0.0)!
Mismatched defaults: Python has True but Dart defaults to false
Unit mismatches: Python uses Duration(milliseconds=150) but Dart uses Duration(microseconds: 150)
Empty collections: field(default_factory=list) means an empty list won't be sent; Dart must handle null with ?? const []
You can find source code for this example here.

Built-in Extensions
Flet controls based on 3rd-party Flutter packages that used to be a part of Flet repository, now have been moved to separate repos and published on pypi:

flet-ads
flet-audio
flet-audio-recorder
flet-camera
flet-charts
flet-datatable2
flet-flashlight
flet-geolocator
flet-lottie
flet-map
flet-permission-handler
flet-rive
flet-secure-storage
flet-video
flet-webview
To use a built-in Flet extension in your project, add it to the dependencies section of your pyproject.toml file, for example:


dependencies = [
  "flet-audio",
  "flet>=0.26.0",
]



