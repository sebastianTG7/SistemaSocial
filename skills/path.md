import flet as ft


def main(page: ft.Page):
    async def handle_pick_files(e: ft.Event[ft.Button]):
        files = await ft.FilePicker().pick_files(allow_multiple=True)
        selected_files.value = (
            ", ".join(map(lambda f: f.name, files)) if files else "Cancelled!"
        )

    async def handle_save_file(e: ft.Event[ft.Button]):
        save_file_path.value = await ft.FilePicker().save_file()

    async def handle_get_directory_path(e: ft.Event[ft.Button]):
        directory_path.value = await ft.FilePicker().get_directory_path()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Button(
                                content="Pick files",
                                icon=ft.Icons.UPLOAD_FILE,
                                on_click=handle_pick_files,
                            ),
                            selected_files := ft.Text(),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Button(
                                content="Save file",
                                icon=ft.Icons.SAVE,
                                on_click=handle_save_file,
                                disabled=page.web,  # disable this button in web mode
                            ),
                            save_file_path := ft.Text(),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Button(
                                content="Open directory",
                                icon=ft.Icons.FOLDER_OPEN,
                                on_click=handle_get_directory_path,
                                disabled=page.web,  # disable this button in web mode
                            ),
                            directory_path := ft.Text(),
                        ]
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)


Pick and upload files
The following example demonstrates multi-file pick and upload app.

#
# Example of picking and uploading files with progress indication
#
# Run this example with:
#    export FLET_SECRET_KEY=<some_secret_key>
#    uv run flet run --web examples/services/file_picker/pick_and_upload/main.py
#
from dataclasses import dataclass, field

import flet as ft


@dataclass
class State:
    file_picker: ft.FilePicker | None = None
    picked_files: list[ft.FilePickerFile] = field(default_factory=list)


state = State()


def main(page: ft.Page):
    if not page.web:
        page.add(
            ft.SafeArea(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "This example is only available in Flet Web mode.\n"
                            "\n"
                            "Run this example with:\n"
                            "    export FLET_SECRET_KEY=<some_secret_key>\n"
                            "    flet run --web "
                            "examples/services/file_picker/pick_and_upload/main.py",
                            color=ft.Colors.RED,
                            selectable=True,
                        )
                    ],
                ),
            )
        )
        return

    prog_bars: dict[str, ft.ProgressRing] = {}

    def on_upload_progress(e: ft.FilePickerUploadEvent):
        prog_bars[e.file_name].value = e.progress

    async def handle_files_pick(e: ft.Event[ft.Button]):
        state.file_picker = ft.FilePicker(on_upload=on_upload_progress)
        files = await state.file_picker.pick_files(allow_multiple=True)
        print("Picked files:", files)
        state.picked_files = files

        # update progress bars
        upload_button.disabled = len(files) == 0
        prog_bars.clear()
        upload_progress.controls.clear()
        for f in files:
            prog = ft.ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
            prog_bars[f.name] = prog
            upload_progress.controls.append(ft.Row([prog, ft.Text(f.name)]))

    async def handle_file_upload(e: ft.Event[ft.Button]):
        upload_button.disabled = True
        await state.file_picker.upload(
            files=[
                ft.FilePickerUploadFile(
                    name=file.name,
                    upload_url=page.get_upload_url(f"dir/{file.name}", 60),
                )
                for file in state.picked_files
            ]
        )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Button(
                        content="Select files...",
                        icon=ft.Icons.FOLDER_OPEN,
                        on_click=handle_files_pick,
                    ),
                    upload_progress := ft.Column(),
                    upload_button := ft.Button(
                        content="Upload",
                        icon=ft.Icons.UPLOAD,
                        on_click=handle_file_upload,
                        disabled=True,
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main, upload_dir="examples")


Pick text content and save/download it
Use pick_files() with with_data=True when you need file contents directly, such as in web apps where FilePickerFile.path is not available.

#
# Example of picking and saving text content with FilePicker.
#
# Run this example with:
#    uv run flet run --web main.py
#
import flet as ft


def main(page: ft.Page):
    selected_file_name = ft.Text("No file selected")
    selected_file_content = ft.TextField(
        label="Selected file content",
        multiline=True,
        min_lines=8,
        max_lines=14,
    )
    save_status = ft.Text()

    async def pick_text_file(_: ft.Event[ft.Button]):
        files = await ft.FilePicker().pick_files(
            allow_multiple=False,
            with_data=True,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt", "md"],
        )
        if not files:
            selected_file_name.value = "Selection cancelled"
            selected_file_content.value = ""
            return

        selected = files[0]
        selected_file_name.value = f"Selected: {selected.name} ({selected.size} bytes)"
        selected_file_content.value = (
            selected.bytes.decode("utf-8", errors="replace") if selected.bytes else ""
        )
        save_status.value = ""

    async def save_text_file(_: ft.Event[ft.Button]):
        file_name = "flet_text_content.txt"
        file_path = await ft.FilePicker().save_file(
            file_name=file_name,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"],
            src_bytes=selected_file_content.value.encode("utf-8"),
        )
        if page.web:
            save_status.value = f"Downloaded as {file_name}"
        else:
            save_status.value = (
                f"Saved to: {file_path}" if file_path else "Save cancelled"
            )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Pick a .txt/.md file and load its text from "
                        "FilePickerFile.bytes"
                    ),
                    ft.Button(
                        content="Pick text file",
                        icon=ft.Icons.UPLOAD_FILE,
                        on_click=pick_text_file,
                    ),
                    selected_file_name,
                    selected_file_content,
                    ft.Button(
                        content="Save / Download text",
                        icon=ft.Icons.DOWNLOAD,
                        on_click=save_text_file,
                    ),
                    save_status,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)

Events
bolt
on_upload
class-attribute
instance-attribute
Copy
on_upload: Optional[EventHandler[FilePickerUploadEvent]] = None
Called when a file is uploaded via upload method.

This callback is invoked at least twice for each uploaded file: once with 0.0 progress before the upload starts, and once with 1.0 progress when the upload completes.

For files larger than 1 MB, additional progress events are emitted at every 10% increment (for example, 0.1, 0.2, ...).

Methods
deployed_code
get_directory_path
async
Copy
get_directory_path(dialog_title: Optional[str] = None, initial_directory: Optional[str] = None)
Selects a directory and returns its absolute path.

Parameters:

dialog_title (Optional[str], default: None) - The title of the dialog window. Defaults to [FilePicker].
initial_directory (Optional[str], default: None) - The initial directory where the dialog should open.
Returns:

Optional[str] - The selected directory path or None if the dialog was cancelled.
Raises:

FletUnsupportedPlatformException - If called in web mode.
deployed_code
pick_files
async
Copy
pick_files(dialog_title: Optional[str] = None, initial_directory: Optional[str] = None, file_type: FilePickerFileType = FilePickerFileType.ANY, allowed_extensions: Optional[list[str]] = None, allow_multiple: bool = False, with_data: bool = False)
Opens a pick file dialog.

Tip
To upload the picked files, pass them to upload method, along with their upload URLs.

Parameters:

dialog_title (Optional[str], default: None) - The title of the dialog window.
initial_directory (Optional[str], default: None) - The initial directory where the dialog should open.
file_type (FilePickerFileType, default: FilePickerFileType.ANY) - The file types allowed to be selected.
allow_multiple (bool, default: False) - Allow the selection of multiple files at once.
with_data (bool, default: False) - Read selected file contents into bytes.
allowed_extensions (Optional[list[str]], default: None) - The allowed file extensions. Has effect only if file_type is flet.FilePickerFileType.CUSTOM.
Returns:

list[FilePickerFile] - A list of selected files.
deployed_code
save_file
async
Copy
save_file(dialog_title: Optional[str] = None, file_name: Optional[str] = None, initial_directory: Optional[str] = None, file_type: FilePickerFileType = FilePickerFileType.ANY, allowed_extensions: Optional[list[str]] = None, src_bytes: Optional[bytes] = None)
Opens a save file dialog which lets the user select a file path and a file name to save a file.

Note
On desktop this method only opens a dialog for the user to select a location and file name, and returns the chosen path. The file itself is not created or saved.
Parameters:

dialog_title (Optional[str], default: None) - The title of the dialog window.
file_name (Optional[str], default: None) - The default file name.
initial_directory (Optional[str], default: None) - The initial directory where the dialog should open.
file_type (FilePickerFileType, default: FilePickerFileType.ANY) - The file types allowed to be selected.
src_bytes (Optional[bytes], default: None) - The contents of a file. Must be provided in web, iOS or Android modes.
allowed_extensions (Optional[list[str]], default: None) - The allowed file extensions. Has effect only if file_type is flet.FilePickerFileType.CUSTOM.
Raises:

ValueError - If src_bytes is not provided, when called in web mode, on iOS or Android.
ValueError - If file_name is not provided in web mode.
deployed_code
upload
async
Copy
upload(files: list[FilePickerUploadFile])
Uploads picked files to specified upload URLs.

Before calling this method, pick_files first has to be called to ensure the internal file picker selection is not empty.

Once called, Flet asynchronously starts uploading selected files one-by-one and reports the progress via on_upload event.

Parameters:

files (list[FilePickerUploadFile]) - A list of FilePickerUploadFile, where each item specifies which file to upload, and where (with PUT or POST).