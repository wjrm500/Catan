class HexagonBorderRender:
    def __init__(self, render):
        self.render = render

    def add_hexagon_border(self):
        rendering = self.render.rendering
        line_width = round(rendering.scale / 10)
        for line in self.render.hexagon.lines:
            tags = [
                rendering.CT_OBJ_HEXAGON, ### Generic Catan hexagon
                self.render.hexagon_tag, ### Unique Catan hexagon
                rendering.ct_line_tag(line), ### Catan line
                rendering.CV_OBJ_LINE ### Canvas line
            ]
            rendering.create_line(rendering.real_x(line.start_node), rendering.real_y(line.start_node), rendering.real_x(line.end_node), rendering.real_y(line.end_node), tags = tags, fill = 'black', width = line_width)
            if line not in self.render.hexagon.focused_lines:
                self.render.hexagon.focused_lines.append(line)
        ### Filler circles to bridge gap between lines, which is especially visible with larger hexagons
        r = line_width / 2.5 ### Circle radius
        for node in self.render.hexagon.nodes:
            tags = [
                rendering.CT_OBJ_HEXAGON, ### Generic Catan hexagon
                self.render.hexagon_tag, ### Unique Catan hexagon
                rendering.ct_node_tag(node), ### Catan node
                rendering.CV_OBJ_OVAL ### Canvas oval
            ]
            x, y = rendering.real_x(node), rendering.real_y(node)
            rendering.create_oval(x - r, y - r, x + r, y + r, tags = tags, fill = 'black', outline = '') 
        
    def remove_hexagon_border(self, hexagons_to_focus = []):
        rendering = self.render.rendering
        focus_retaining_lines = [line for hexagon in hexagons_to_focus for line in hexagon.lines]
        line_width = round(rendering.scale / 10)
        for line in self.render.hexagon.lines:
            line_tag = rendering.ct_line_tag(line)
            rendering.delete_tag(line_tag)
            for node in line.nodes:
                node_tag = rendering.ct_node_tag(node)
                rendering.delete_tag(node_tag)
            if line in focus_retaining_lines:
                tags = [
                    rendering.CT_OBJ_HEXAGON, ### Generic Catan hexagon
                    self.render.hexagon_tag, ### Unique Catan hexagon
                    line_tag, ### Catan line
                    rendering.CV_OBJ_LINE ### Canvas line
                ]
                rendering.create_line(rendering.real_x(line.start_node), rendering.real_y(line.start_node), rendering.real_x(line.end_node), rendering.real_y(line.end_node), tags = tags, fill = 'black', width = line_width)
                r = line_width / 2.5 ### Circle radius
                for node in line.nodes:
                    tags = [
                        rendering.CT_OBJ_HEXAGON, ### Generic Catan hexagon
                        self.render.hexagon_tag, ### Unique Catan hexagon
                        rendering.ct_node_tag(node), ### Catan node
                        rendering.CV_OBJ_OVAL ### Canvas oval
                    ]
                    x, y = rendering.real_x(node), rendering.real_y(node)
                    rendering.create_oval(x - r, y - r, x + r, y + r, tags = tags, fill = 'black', outline = '')