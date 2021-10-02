class HexagonBorderRender:
    def __init__(self, render):
        self.render = render

    def add_hexagon_border(self):
        show_line_ids = False
        line_width = round(self.render.rendering.scale / 10)
        for line in self.render.hexagon.lines:
            line_tag = self.render.line_tag(line)
            tags = [self.render.rendering.OBJECT_LINE, line_tag]
            self.render.rendering.create_line(line.start_node.real_x, line.start_node.real_y, line.end_node.real_x, line.end_node.real_y, tags = tags, fill = 'black', width = line_width)
            if show_line_ids:
                (x, y) = line.centre_point(True)
                circle_radius = 10
                tags = [self.render.rendering.OBJECT_OVAL]
                self.render.rendering.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, tags = tags, fill = 'white', width = 1)
                font_size = round(self.render.rendering.scale / 4)
                self.render.rendering.create_text(x, y, fill = 'black', font = 'Arial {} bold'.format(font_size), text = line.id)
            if line not in self.render.hexagon.focused_lines:
                self.render.hexagon.focused_lines.append(line)
        ### Filler circles to bridge gap between lines, which is especially visible with larger hexagons
        r = line_width / 2
        for node in self.render.hexagon.nodes:
            tags = [self.render.rendering.OBJECT_OVAL]
            self.render.rendering.create_oval(node.real_x - r, node.real_y - r, node.real_x + r, node.real_y + r, tags = tags, fill = 'black', outline = '') 
    
    def remove_hexagon_border(self, hexagons_to_focus = []):
        all_focused_lines = [line for hexagon in hexagons_to_focus for line in hexagon.lines]
        line_width = round(self.render.rendering.scale / 10)
        for line in self.render.hexagon.focused_lines:
            line_tag = self.render.line_tag(line)
            self.render.rendering.delete_tag(line_tag)
            for node in line.nodes:
                node_tag = self.render.node_tag(node)
                self.render.rendering.delete_tag(node_tag)
            if line in all_focused_lines:
                tags = [self.render.rendering.OBJECT_LINE, line_tag]
                self.render.rendering.create_line(line.start_node.real_x, line.start_node.real_y, line.end_node.real_x, line.end_node.real_y, tags = tags, fill = 'black', width = line_width)
                r = line_width / 2
                for node in line.nodes:
                    node_tag = self.render.node_tag(node)
                    tags = [self.render.rendering.OBJECT_OVAL, node_tag]
                    self.render.rendering.create_oval(node.real_x - r, node.real_y - r, node.real_x + r, node.real_y + r, tags = tags, fill = 'black', outline = '')
        self.render.hexagon.focused_lines = [line for line in self.render.hexagon.focused_lines if line in all_focused_lines]