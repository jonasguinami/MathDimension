import tkinter
import customtkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp

# --- Configurações de Aparência ---
BG_COLOR = "#f2f2f2"
FRAME_COLOR = "#ffffff"
TEXT_COLOR = "#2b2b2b"
ACCENT_COLOR = "#4a90e2"
PLOT_BG_COLOR = "#ffffff"

class GraphingCalculator3DApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Análise Gráfica 3D")
        self.geometry("900x750")
        self.configure(fg_color=BG_COLOR)

        # --- Estrutura da Janela ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Frame de Controle (Topo) ---
        self.control_frame = customtkinter.CTkFrame(self, fg_color=FRAME_COLOR, corner_radius=10)
        self.control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.control_frame.grid_columnconfigure(1, weight=1)

        # Entrada da Equação Principal
        self.label_f = customtkinter.CTkLabel(self.control_frame, text="f(x, y) = ", font=("Arial", 14))
        self.label_f.grid(row=0, column=0, padx=(15, 5), pady=10)
        
        self.f_entry = customtkinter.CTkEntry(self.control_frame, placeholder_text="Função Principal (ex: sin(x) * cos(y))", font=("Arial", 14), border_width=1, corner_radius=8)
        self.f_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
        self.f_entry.bind("<Return>", lambda event: self.plot_graph())

        self.plot_button = customtkinter.CTkButton(self.control_frame, text="Plotar Gráfico", command=self.plot_graph, corner_radius=8, fg_color=ACCENT_COLOR)
        self.plot_button.grid(row=0, column=2, padx=(5, 15), pady=10)
        
        # --- Sistema de Abas ---
        self.tab_view = customtkinter.CTkTabview(self, fg_color=FRAME_COLOR)
        self.tab_view.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.tab_graph = self.tab_view.add("Gráfico 3D")
        self.tab_steps = self.tab_view.add("Passo a Passo")
        self.tab_analysis = self.tab_view.add("Análise de Funções")

        # --- Configuração da Aba "Gráfico 3D" ---
        self.fig = plt.Figure(figsize=(5, 4), dpi=100, facecolor=PLOT_BG_COLOR)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_graph)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # --- Configuração da Aba "Passo a Passo" ---
        self.steps_textbox = customtkinter.CTkTextbox(self.tab_steps, font=("Arial", 14), wrap="word", fg_color="#e9e9e9", text_color=TEXT_COLOR)
        self.steps_textbox.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Configuração da Aba "Análise de Funções" ---
        self.analysis_frame = customtkinter.CTkFrame(self.tab_analysis, fg_color="transparent")
        self.analysis_frame.pack(fill="x", padx=10, pady=10)
        self.analysis_frame.grid_columnconfigure(1, weight=1)

        self.label_g = customtkinter.CTkLabel(self.analysis_frame, text="g(x, y) = ", font=("Arial", 14))
        self.label_g.grid(row=0, column=0, padx=(5, 5), pady=10)
        
        self.g_entry = customtkinter.CTkEntry(self.analysis_frame, placeholder_text="Função Secundária (ex: x**2 + y**2)", font=("Arial", 14), border_width=1, corner_radius=8)
        self.g_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=10)

        self.operator_var = customtkinter.StringVar(value="+")
        operators = ["+", "-", "*", "/"]
        for i, op in enumerate(operators):
            radio = customtkinter.CTkRadioButton(self.analysis_frame, text=op, variable=self.operator_var, value=op)
            radio.grid(row=0, column=i+2, padx=5)

        self.mix_button = customtkinter.CTkButton(self.analysis_frame, text="Misturar", command=self.plot_analysis, corner_radius=8)
        self.mix_button.grid(row=0, column=len(operators)+2, padx=15)

        # Label para mensagens de erro
        self.error_label = customtkinter.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")
        
        # Plota um gráfico de exemplo ao iniciar
        self.f_entry.insert(0, "sin(sqrt(x**2 + y**2))")
        self.g_entry.insert(0, "exp(-(x**2 + y**2)/4)")
        self.plot_graph()

    def parse_equation(self, eq_str):
        """Função central para analisar e converter uma string em uma expressão SymPy."""
        x_sym, y_sym = sp.symbols('x y')
        allowed_functions = {
            "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
            "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh, "exp": sp.exp, "log": sp.log, "pi": sp.pi, "sqrt": sp.sqrt
        }
        return sp.sympify(eq_str, locals=allowed_functions)

    def plot_graph(self):
        """Plota o gráfico da função principal f(x, y)."""
        self.error_label.configure(text="")
        eq_str = self.f_entry.get()
        if not eq_str:
            self.error_label.configure(text="Por favor, insira a função principal f(x, y).")
            return

        try:
            expr = self.parse_equation(eq_str)
            self.update_plot_and_steps(expr, eq_str)
            self.tab_view.set("Gráfico 3D")
        except Exception as e:
            self.error_label.configure(text=f"Erro na equação: {e}")

    def plot_analysis(self):
        """Plota o gráfico da combinação de f(x, y) e g(x, y)."""
        self.error_label.configure(text="")
        f_str = self.f_entry.get()
        g_str = self.g_entry.get()
        op = self.operator_var.get()

        if not f_str or not g_str:
            self.error_label.configure(text="Por favor, insira ambas as funções para análise.")
            return

        try:
            f_expr = self.parse_equation(f_str)
            g_expr = self.parse_equation(g_str)
            
            if op == '+': combined_expr = f_expr + g_expr
            elif op == '-': combined_expr = f_expr - g_expr
            elif op == '*': combined_expr = f_expr * g_expr
            elif op == '/': combined_expr = f_expr / g_expr
            
            combined_str = f"({f_str}) {op} ({g_str})"
            self.update_plot_and_steps(combined_expr, combined_str)
            self.tab_view.set("Gráfico 3D")
        except Exception as e:
            self.error_label.configure(text=f"Erro na equação: {e}")

    def update_plot_and_steps(self, expr, eq_str):
        """Atualiza o gráfico 3D e a aba de passo a passo com a expressão fornecida."""
        x_sym, y_sym = sp.symbols('x y')
        
        # --- Atualiza o Gráfico 3D ---
        f = sp.lambdify((x_sym, y_sym), expr, 'numpy')
        x_vals = np.linspace(-10, 10, 100)
        y_vals = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = f(X, Y)

        self.ax.clear()
        self.ax.set_facecolor(PLOT_BG_COLOR)
        self.ax.set_xlabel("Eixo X"); self.ax.set_ylabel("Eixo Y"); self.ax.set_zlabel("Z")
        self.ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.9)
        self.fig.tight_layout()
        self.canvas.draw()

        # --- Atualiza a Aba Passo a Passo ---
        self.steps_textbox.delete("1.0", "end")
        steps = [
            f"Equação Fornecida:\n  f(x, y) = {eq_str}\n\n",
            "1. Análise (Parsing):\n  O sistema lê a string e a converte em uma expressão matemática simbólica usando a biblioteca SymPy. Isso garante que a equação seja matematicamente válida e segura.\n\n",
            f"  Expressão SymPy: {expr}\n\n",
            "2. Geração da Grade de Pontos:\n  O sistema cria uma grade de pontos nos eixos X e Y. Para esta visualização, criamos uma grade de 100x100 pontos, variando de -10 a 10 em ambos os eixos.\n\n",
            "3. Cálculo dos Valores de Z:\n  A expressão matemática é aplicada a cada par de coordenadas (x, y) na grade para calcular o valor correspondente de Z. Isso gera uma matriz de 100x100 valores de altura.\n\n",
            "4. Renderização da Superfície:\n  Finalmente, o Matplotlib usa as matrizes de X, Y e Z para desenhar uma superfície 3D, conectando os pontos adjacentes para criar a paisagem visual. Uma paleta de cores ('viridis') é usada para representar a altura (valores de Z)."
        ]
        for step in steps:
            self.steps_textbox.insert("end", step)

    def on_closing(self):
        self.quit()
        self.destroy()

if __name__ == "__main__":
    customtkinter.set_appearance_mode("Light")
    app = GraphingCalculator3DApp()
    app.mainloop()
