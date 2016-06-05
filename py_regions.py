import sublime, sublime_plugin
import re

def get_view_text(view):
    return view.substr(sublime.Region(0, view.size()))

def get_cursor(view):
    return [region.begin() for region in view.sel()]

class Info:
    PLUGIN_NAME = "PyRegions"
    names = []

class PyRegionsMarkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        Info.names = []
        self.view.erase_regions(Info.PLUGIN_NAME)
        regions = []
        contents = get_view_text(self.view)
        matches = re.finditer(r'#region:(.*?)$(.|[\n])*?#endregion:\1', contents, re.M)
        for match in matches:
            region = sublime.Region(match.start(), match.end())
            Info.names.append(match.group(1))
            lines = self.view.lines(region)
            region = sublime.Region(lines[0].b, lines[-1].b)
            regions.append(region)
        self.view.add_regions(Info.PLUGIN_NAME, regions, "comment", "bookmark", sublime.HIDDEN)

class PyRegionsToggleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('py_regions_mark')
        cursors = get_cursor(self.view)
        for cursor in cursors:
            for region in self.view.get_regions(Info.PLUGIN_NAME):
                lines = self.view.lines(region)
                start, end = lines[0].a, lines[-1].b
                if start <= cursor <= end:
                    if not self.view.fold(region):
                        self.view.unfold(region)
                    break

class PyRegionsListener(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        view.run_command('py_regions_mark')
        status_set = False
        cursors = get_cursor(view)
        for cursor in cursors:
            for index, region in enumerate(view.get_regions(Info.PLUGIN_NAME)):
                lines = view.lines(region)
                start, end = lines[0].a, lines[-1].b
                if start <= cursor <= end:
                    view.set_status(Info.PLUGIN_NAME, "Region: " + Info.names[index])
                    status_set = True
        if not status_set:
            view.erase_status(Info.PLUGIN_NAME)

    def on_load(self, view):
        view.run_command('py_regions_mark')

    def on_pre_save(self, view):
        view.run_command('py_regions_mark')