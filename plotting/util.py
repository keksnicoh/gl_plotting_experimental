

function_kernel = lambda f: "vec4 f(vec4 x) { return vec4(x.x, "+f+", 0,1); }"

class UniformManager():
    def __init__(self, global_uniforms={}, local_uniforms={}):
        self.global_uniforms = global_uniforms
        self.local_uniforms = local_uniforms
        self._updated = False
        self.global_uniforms_steps = {}
    def has_updated(self):
        updated = self._updated
        self._updated = False
        return updated
    def get_global_uniforms(self):
        return self.global_uniforms

    def get_local_uniforms(self):
        return self.local_uniforms

    def get_global(self, name): return self.global_uniforms[name]

    def set_global(self, name, value, steps=1):
        self._updated = True
        self.global_uniforms[name] = value
        self.global_uniforms_steps[name] = steps

    def set_local(self, plot, name, value):
        self._updated = True
        if plot not in self.local_uniforms:
            self.local_uniforms[plot] = {}
        self.local_uniforms[plot][name] = value

    def get_local(self, plot, name):

        return self.local_uniforms[plot][name]
