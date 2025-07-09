import tkinter as tk
from tkinter import ttk
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

TOP10 = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B', 'LLY', 'JPM']

def get_market_caps():
    market_caps = []
    names = []
    for ticker in TOP10:
        stock = yf.Ticker(ticker)
        info = stock.info
        cap = info.get('marketCap', 0)
        name = info.get('shortName', ticker)
        market_caps.append(cap)
        names.append(name)
    return names, market_caps

def show_market_cap_graph():
    names, market_caps = get_market_caps()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(names, [cap/1e12 for cap in market_caps], color='skyblue')
    ax.set_ylabel('Market Cap (Trillions USD)')
    ax.set_title('Top 10 Companies by Market Cap')
    ax.set_xticklabels(names, rotation=45, ha='right')
    plt.tight_layout()

    # Embed the plot in Tkinter
    for widget in graph_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root = tk.Tk()
root.title("Top 10 Companies Finance Info")

main_frame = ttk.Frame(root)
main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

graph_frame = ttk.Frame(main_frame)
graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

btn = ttk.Button(root, text="Show Market Cap Graph", command=show_market_cap_graph)
btn.pack(side=tk.BOTTOM, pady=10)

root.mainloop()