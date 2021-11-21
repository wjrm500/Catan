### TODO: Do we even need all this stuff? Is line width not a create_polygon param? Only thing to keep is drawing outline of whole board?
class HexagonBorderRender:
    def __init__(self, render):
        self.render = render
    
    def draw_focused_line(self, line, line_tag, line_width, coastline = False):
        rendering = self.render.rendering
        tags = [
            rendering.CT_OBJ_HEXAGON, ### Generic Catan hexagon
            self.render.hexagon_tag, ### Unique Catan hexagon
            rendering.CV_OBJ_LINE ### Canvas line
        ]
        if not coastline:
            tags.append(line_tag) ### Catan line
        rendering.create_line(rendering.real_x(line.start_node), rendering.real_y(line.start_node), rendering.real_x(line.end_node), rendering.real_y(line.end_node), tags = tags, fill = 'black', width = line_width)
        
        ### Filler circles to bridge gap between lines, which is especially visible with larger hexagons
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
        
    def thicken_coastlines(self):
        rendering = self.render.rendering
        line_width = round(rendering.scale / 30)
        for line in self.render.hexagon.lines:
            if not line.on_coast():
                continue
            line_tag = rendering.ct_line_tag(line)
            self.draw_focused_line(line, line_tag, line_width, coastline = True)

    def add_focused_hexagon_border(self):
        rendering = self.render.rendering
        line_width = round(rendering.scale / 10)
        for line in self.render.hexagon.lines:
            line_tag = rendering.ct_line_tag(line)
            self.draw_focused_line(line, line_tag, line_width, coastline = False)
        
    def remove_focused_hexagon_border(self, hexagons_to_focus = []):
        rendering = self.render.rendering
        focus_retaining_lines = [line for hexagon in hexagons_to_focus for line in hexagon.lines]
        focus_retaining_nodes = [node for hexagon in hexagons_to_focus for node in hexagon.nodes]
        for line in self.render.hexagon.lines:
            if line in focus_retaining_lines:
                continue
            line_tag = rendering.ct_line_tag(line)
            rendering.delete_tag(line_tag)
            for node in line.nodes:
                if node in focus_retaining_nodes:
                    continue
                node_tag = rendering.ct_node_tag(node)
                rendering.delete_tag(node_tag)