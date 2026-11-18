import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Parâmetros de Corte MAPAL", page_icon="⚙️", layout="wide")

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        padding-left: 0.75rem;
        padding-right: 0.75rem;
        max-width: 100% !important;
    }
    iframe {
        height: 100vh !important;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

html_content = '''
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>Parâmetros de Corte MAPAL</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 0; height: 100vh; overflow: hidden; }
    </style>
</head>
<body class="h-screen p-2 flex flex-col box-border">
    <div class="w-full h-full flex flex-col gap-2">
        <!-- Header Compacto -->
        <header class="bg-slate-800 px-4 py-2 rounded-lg border border-slate-700 flex justify-between items-center shrink-0">
            <h1 class="text-base font-bold text-white">Parâmetros de Corte MAPAL</h1>
            <button onclick="toggleFullScreen()" class="bg-slate-700 hover:bg-slate-600 px-2.5 py-1 rounded-md text-xs font-medium text-white transition flex items-center gap-1.5">
                <span>⛶</span> Ecrã Inteiro / Janela
            </button>
        </header>

        <!-- Layout Principal em Grid de Altura Total -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-3 flex-1 min-h-0">
            <!-- Painel de Controlo (Esquerda) -->
            <div class="lg:col-span-4 bg-slate-800 p-3.5 rounded-lg border border-slate-700 flex flex-col gap-2.5 overflow-y-auto min-h-0">
                <h2 class="text-xs font-semibold text-blue-400 uppercase tracking-wider shrink-0">Configuração da Operação</h2>
                
                <!-- 1. Linha de Ferramenta -->
                <div class="space-y-1 shrink-0">
                    <label class="text-[11px] font-medium text-slate-300">1. LINHA DE FERRAMENTA</label>
                    <select id="linha" class="w-full bg-slate-900 border border-slate-700 rounded-md p-1.5 text-xs text-white focus:outline-none focus:border-blue-500" onchange="atualizarFiltroBrocas()">
                        <option value="expert">Expert Line (Alta Performance)</option>
                        <option value="performance">Performance Line</option>
                        <option value="basic">Basic Line (Uso Geral)</option>
                    </select>
                </div>

                <!-- 2. Tipo de Operação / Categoria -->
                <div class="space-y-1 shrink-0">
                    <label class="text-[11px] font-medium text-slate-300">2. TIPO DE OPERAÇÃO / CATEGORIA</label>
                    <select id="categoria" class="w-full bg-slate-900 border border-slate-700 rounded-md p-1.5 text-xs text-white focus:outline-none focus:border-blue-500" onchange="atualizarFiltroBrocas()">
                        <option value="solid">Solid Carbide / Standard Drilling</option>
                        <option value="insert">Insert Drilling (Pastilhas Amovíveis)</option>
                        <option value="spot">Spot Drilling (Centragem / Ponto)</option>
                        <option value="stepped">Stepped Drilling (Escalonada)</option>
                        <option value="deep">Deep Drilling (Furação Profunda)</option>
                        <option value="reaming">Drill Reaming (Alargamento)</option>
                    </select>
                </div>

                <!-- 3. Refrigeração Disponível -->
                <div class="space-y-1 shrink-0">
                    <label class="text-[11px] font-medium text-slate-300">3. REFRIGERAÇÃO DISPONÍVEL</label>
                    <select id="filtro-refrig" class="w-full bg-slate-900 border border-slate-700 rounded-md p-1.5 text-xs text-white focus:outline-none focus:border-blue-500" onchange="atualizarFiltroBrocas()">
                        <option value="com">Com Refrigeração Interna</option>
                        <option value="sem">Sem Refrigeração Interna</option>
                    </select>
                </div>

                <!-- 4. Modelo de Ferramenta -->
                <div class="space-y-1 shrink-0">
                    <label class="text-[11px] font-medium text-slate-300">4. MODELO DE FERRAMENTA</label>
                    <select id="broca" class="w-full bg-slate-900 border border-slate-700 rounded-md p-1.5 text-xs text-white focus:outline-none focus:border-blue-500" onchange="mudarBroca()">
                    </select>
                </div>

                <!-- 5. Grupo de Materiais -->
                <div class="space-y-1 shrink-0">
                    <label class="text-[11px] font-medium text-slate-300">5. GRUPO DE MATERIAIS (MMG)</label>
                    <select id="grupo" class="w-full bg-slate-900 border border-slate-700 rounded-md p-1.5 text-xs text-white focus:outline-none focus:border-blue-500" onchange="mudarGrupoMaterial()">
                    </select>
                </div>

                <!-- Checkbox regra de liga MAPAL -->
                <div class="bg-slate-900 p-2 rounded-md border border-slate-700/80 space-y-0.5 shrink-0">
                    <label class="flex items-start gap-1.5 cursor-pointer text-[11px] text-slate-300">
                        <input type="checkbox" id="liga-check" class="mt-0.5 rounded bg-slate-800 border-slate-600 text-blue-600 focus:ring-0" onchange="atualizarCalculo()">
                        <span><strong>Soma liga (Cr, Mo, Ni, V, W) > 8%</strong><br><span class="text-[9px] text-amber-400">Regra MAPAL: avança para o grupo seguinte.</span></span>
                    </label>
                </div>

                <!-- 6. Método de Refrigeração -->
                <div class="space-y-1 shrink-0">
                    <label class="text-[11px] font-medium text-slate-300">6. MÉTODO DE REFRIGERAÇÃO A USAR</label>
                    <div class="grid grid-cols-4 gap-1 bg-slate-900 p-1 rounded-md border border-slate-700 text-[11px] text-center font-medium">
                        <button type="button" onclick="setRefrig('int')" id="ref-int" class="py-1.5 rounded bg-blue-600 text-white transition">Interna</button>
                        <button type="button" onclick="setRefrig('ext')" id="ref-ext" class="py-1.5 rounded text-slate-400 hover:text-white transition">Externa</button>
                        <button type="button" onclick="setRefrig('mql')" id="ref-mql" class="py-1.5 rounded text-slate-400 hover:text-white transition">MQL</button>
                        <button type="button" onclick="setRefrig('ar')" id="ref-ar" class="py-1.5 rounded text-slate-400 hover:text-white transition">Ar</button>
                    </div>
                    <p id="aviso-refrig" class="text-[9px] text-amber-400 hidden">Nota: Esta ferramenta não permite refrigeração interna.</p>
                </div>

                <!-- 7. Diâmetro Pretendido, Profundidade, Densidade e Preço Sucata -->
                <div class="grid grid-cols-2 gap-2 shrink-0">
                    <div class="space-y-1">
                        <label class="text-[11px] font-medium text-slate-300">7. DIÂMETRO (Ø)</label>
                        <div class="flex items-center gap-1">
                            <button onclick="ajustarDiametro(-0.5)" class="bg-slate-700 hover:bg-slate-600 px-2 py-1.5 rounded-md text-white font-bold text-xs">-</button>
                            <input type="number" id="diametro" value="8.00" step="0.1" min="1" max="30" class="w-full bg-slate-900 border border-slate-700 rounded-md p-1.5 text-center text-sm font-bold text-white focus:outline-none focus:border-blue-500" oninput="atualizarCalculo()">
                            <button onclick="ajustarDiametro(0.5)" class="bg-slate-700 hover:bg-slate-600 px-2 py-1.5 rounded-md text-white font-bold text-xs">+</button>
                        </div>
                    </div>
                    <div class="space-y-1">
                        <label class="text-[11px] font-medium text-slate-300">8. PROFUNDIDADE (L)</label>
                        <div class="flex items-center gap-1">
                            <input type="number" id="profundidade" value="25.0" step="1" min="0.1" max="500" class="w-full bg-slate-900 border border-slate-700 rounded-md p-1.5 text-center text-sm font-bold text-white focus:outline-none focus:border-blue-500" oninput="atualizarCalculo()">
                            <span class="text-[10px] text-slate-400 font-medium">mm</span>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-2 shrink-0 pt-1">
                    <div class="space-y-1">
                        <label class="text-[11px] font-medium text-slate-300">9. DENSIDADE (g/cm³)</label>
                        <input type="number" id="densidade" value="7.85" step="0.01" min="0.5" max="25" class="w-full bg-slate-900 border border-slate-700 rounded-md p-1.5 text-center text-xs font-bold text-white focus:outline-none focus:border-blue-500" oninput="atualizarCalculo()">
                    </div>
                    <div class="space-y-1">
                        <label class="text-[11px] font-medium text-slate-300">10. VALOR SUCATA (€/kg)</label>
                        <input type="number" id="preco-sucata" value="0.35" step="0.05" min="0" max="50" class="w-full bg-slate-900 border border-slate-700 rounded-md p-1.5 text-center text-xs font-bold text-white focus:outline-none focus:border-blue-500" oninput="atualizarCalculo()">
                    </div>
                </div>

                <!-- Ajustes Percentuais (%) -->
                <div class="space-y-2 pt-1 border-t border-slate-700 shrink-0">
                    <label class="text-[11px] font-medium text-blue-400 uppercase tracking-wider">Ajustes Percentuais (%)</label>
                    <div class="space-y-1">
                        <div class="flex justify-between text-[11px] text-slate-300">
                            <span>Ajuste Vc (%):</span>
                            <span id="vc-pct-val" class="font-bold text-cyan-400">0%</span>
                        </div>
                        <div class="flex items-center gap-1.5">
                            <button onclick="ajustarPct('vc', -1)" class="bg-slate-700 hover:bg-slate-600 px-2 py-0.5 rounded text-white text-[10px] font-bold">-1%</button>
                            <input type="range" id="vc-slider" min="-50" max="50" value="0" step="1" class="w-full accent-blue-500" oninput="onSliderVc()">
                            <button onclick="ajustarPct('vc', 1)" class="bg-slate-700 hover:bg-slate-600 px-2 py-0.5 rounded text-white text-[10px] font-bold">+1%</button>
                            <button onclick="resetPct('vc')" class="bg-slate-900 border border-slate-600 text-slate-400 hover:text-white px-1.5 py-0.5 rounded text-[10px]">Reset</button>
                        </div>
                    </div>
                    <div class="space-y-1">
                        <div class="flex justify-between text-[11px] text-slate-300">
                            <span>Ajuste Avanço f (%):</span>
                            <span id="f-pct-val" class="font-bold text-cyan-400">0%</span>
                        </div>
                        <div class="flex items-center gap-1.5">
                            <button onclick="ajustarPct('f', -1)" class="bg-slate-700 hover:bg-slate-600 px-2 py-0.5 rounded text-white text-[10px] font-bold">-1%</button>
                            <input type="range" id="f-slider" min="-50" max="50" value="0" step="1" class="w-full accent-blue-500" oninput="onSliderF()">
                            <button onclick="ajustarPct('f', 1)" class="bg-slate-700 hover:bg-slate-600 px-2 py-0.5 rounded text-white text-[10px] font-bold">+1%</button>
                            <button onclick="resetPct('f')" class="bg-slate-900 border border-slate-600 text-slate-400 hover:text-white px-1.5 py-0.5 rounded text-[10px]">Reset</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Resultados e Indicadores (Direita) -->
            <div class="lg:col-span-8 flex flex-col gap-3 min-h-0 overflow-y-auto">
                <!-- Grid de Métricas CNC Principal -->
                <div class="grid grid-cols-2 md:grid-cols-5 gap-3 shrink-0">
                    <!-- Cartão f -->
                    <div id="card-f" class="bg-slate-800 p-3 rounded-lg border border-slate-700 transition-colors">
                        <div class="flex justify-between items-center">
                            <span class="text-[11px] text-slate-400">Avanço (f)</span>
                            <button type="button" onclick="toggleLock('f')" id="btn-lock-f" title="Desbloquear para edição manual" class="text-xs px-1 py-0.5 rounded bg-slate-900/80 border border-slate-700 hover:border-slate-500 transition">🔒</button>
                        </div>
                        <input type="number" id="input-f" value="0.3850" step="0.005" min="0.001" readonly oninput="onManualInput('f')" class="w-full bg-transparent text-xl font-bold text-white mt-0.5 focus:outline-none rounded px-1 -ml-1">
                        <div class="flex justify-between items-center mt-0.5">
                            <span class="text-[9px] text-blue-400">mm/rot</span>
                            <span id="status-f" class="text-[9px] text-slate-500">Auto</span>
                        </div>
                    </div>

                    <!-- Cartão Vc -->
                    <div id="card-vc" class="bg-slate-800 p-3 rounded-lg border border-slate-700 transition-colors">
                        <div class="flex justify-between items-center">
                            <span class="text-[11px] text-slate-400">Vc</span>
                            <button type="button" onclick="toggleLock('vc')" id="btn-lock-vc" title="Desbloquear para edição manual" class="text-xs px-1 py-0.5 rounded bg-slate-900/80 border border-slate-700 hover:border-slate-500 transition">🔒</button>
                        </div>
                        <input type="number" id="input-vc" value="105" step="1" min="1" readonly oninput="onManualInput('vc')" class="w-full bg-transparent text-xl font-bold text-white mt-0.5 focus:outline-none rounded px-1 -ml-1">
                        <div class="flex justify-between items-center mt-0.5">
                            <span class="text-[9px] text-slate-400">m/min</span>
                            <span id="status-vc" class="text-[9px] text-slate-500">Auto</span>
                        </div>
                    </div>

                    <!-- Rotações Limite da Máquina (Com Cadeado) -->
                    <div id="card-rpm-max" class="bg-slate-800 p-3 rounded-lg border border-slate-700 transition-colors">
                        <div class="flex justify-between items-center">
                            <span class="text-[11px] text-slate-400">RPM Máx. Máquina</span>
                            <button type="button" onclick="toggleLock('rpm-max')" id="btn-lock-rpm-max" title="Desbloquear para definir limite de RPM" class="text-xs px-1 py-0.5 rounded bg-slate-900/80 border border-slate-700 hover:border-slate-500 transition">🔒</button>
                        </div>
                        <input type="number" id="input-rpm-max" value="8000" step="100" min="100" max="60000" readonly oninput="onManualInput('rpm-max')" class="w-full bg-transparent text-xl font-bold text-white mt-0.5 focus:outline-none rounded px-1 -ml-1">
                        <div class="flex justify-between items-center mt-0.5">
                            <span class="text-[9px] text-slate-400">rpm</span>
                            <span id="status-rpm-max" class="text-[9px] text-slate-500">Inativo</span>
                        </div>
                    </div>

                    <!-- Rotações (Spindle) -->
                    <div class="bg-slate-800 p-3 rounded-lg border border-slate-700">
                        <span class="text-[11px] text-slate-400">Rotações (Spindle)</span>
                        <div class="text-xl font-bold text-white mt-0.5" id="res-n">4178</div>
                        <span class="text-[9px] text-slate-400">rpm</span>
                    </div>

                    <!-- Avanço de Trabalho -->
                    <div class="bg-slate-800 p-3 rounded-lg border border-slate-700">
                        <span class="text-[11px] text-slate-400">Avanço Trabalho</span>
                        <div class="text-xl font-bold text-white mt-0.5" id="res-vf">1608</div>
                        <span class="text-[9px] text-slate-400">mm/min</span>
                    </div>
                </div>

                <!-- Indicadores de Tempo de Furação e Volume Removido -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 shrink-0">
                    <div class="bg-gradient-to-r from-blue-900/40 to-slate-800 p-3 rounded-lg border border-blue-700/50 flex justify-between items-center">
                        <div>
                            <span class="text-[11px] text-blue-300 font-semibold uppercase tracking-wider">⏱️ Tempo de Furação (Ciclo)</span>
                            <div class="text-2xl font-extrabold text-white mt-0.5" id="res-tempo">0.00 <span class="text-sm font-normal text-slate-300">seg</span></div>
                        </div>
                        <div class="text-right">
                            <span class="text-[10px] text-slate-400">Curso Efetivo (Le)</span>
                            <div class="text-xs font-mono font-bold text-cyan-400" id="res-curso">27.40 mm</div>
                        </div>
                    </div>
                    <div class="bg-gradient-to-r from-emerald-900/40 to-slate-800 p-3 rounded-lg border border-emerald-700/50 flex justify-between items-center">
                        <div>
                            <span class="text-[11px] text-emerald-300 font-semibold uppercase tracking-wider">📦 Volume de Material Removido</span>
                            <div class="text-2xl font-extrabold text-white mt-0.5" id="res-volume">1256.6 <span class="text-sm font-normal text-slate-300">mm³</span></div>
                        </div>
                        <div class="text-right">
                            <span class="text-[10px] text-slate-400">Taxa de Remoção</span>
                            <div class="text-xs font-mono font-bold text-emerald-400" id="res-taxa">-- cm³/min</div>
                        </div>
                    </div>
                </div>

                <!-- Novos Indicadores: Peso Removido e Lucro de Sucata -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 shrink-0">
                    <div class="bg-gradient-to-r from-cyan-900/40 to-slate-800 p-3 rounded-lg border border-cyan-700/50 flex justify-between items-center">
                        <div>
                            <span class="text-[11px] text-cyan-300 font-semibold uppercase tracking-wider">⚖️ Peso de Limalha Removida</span>
                            <div class="text-2xl font-extrabold text-white mt-0.5" id="res-peso">0.000 <span class="text-sm font-normal text-slate-300">kg</span></div>
                        </div>
                        <div class="text-right">
                            <span class="text-[10px] text-slate-400">Massa por Furo</span>
                            <div class="text-xs font-mono font-bold text-cyan-400" id="res-peso-g">0.00 g</div>
                        </div>
                    </div>
                    <div class="bg-gradient-to-r from-teal-900/40 to-slate-800 p-3 rounded-lg border border-teal-700/50 flex justify-between items-center">
                        <div>
                            <span class="text-[11px] text-teal-300 font-semibold uppercase tracking-wider">💶 Valor/Lucro de Sucata (por Furo)</span>
                            <div class="text-2xl font-extrabold text-white mt-0.5" id="res-sucata-val">0.00 <span class="text-sm font-normal text-slate-300">€</span></div>
                        </div>
                        <div class="text-right">
                            <span class="text-[10px] text-slate-400">Retorno Comercial</span>
                            <div class="text-xs font-mono font-bold text-teal-400" id="res-sucata-lote">0.00 € / 1000 furos</div>
                        </div>
                    </div>
                </div>

                <!-- Indicadores: Força de Furação e Binário de Corte -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 shrink-0">
                    <div class="bg-gradient-to-r from-amber-900/40 to-slate-800 p-3 rounded-lg border border-amber-700/50 flex justify-between items-center">
                        <div>
                            <span class="text-[11px] text-amber-300 font-semibold uppercase tracking-wider">⚡ Força de Avanço Estimada (Ff)</span>
                            <div class="text-2xl font-extrabold text-white mt-0.5" id="res-forca">0 <span class="text-sm font-normal text-slate-300">N</span></div>
                        </div>
                        <div class="text-right">
                            <span class="text-[10px] text-slate-400">Esforço Axial</span>
                            <div class="text-xs font-mono font-bold text-amber-400" id="res-forca-kgf">0 kgf</div>
                        </div>
                    </div>
                    <div class="bg-gradient-to-r from-purple-900/40 to-slate-800 p-3 rounded-lg border border-purple-700/50 flex justify-between items-center">
                        <div>
                            <span class="text-[11px] text-purple-300 font-semibold uppercase tracking-wider">🔄 Binário de Corte Estimado (Mc)</span>
                            <div class="text-2xl font-extrabold text-white mt-0.5" id="res-binario">0.0 <span class="text-sm font-normal text-slate-300">N·m</span></div>
                        </div>
                        <div class="text-right">
                            <span class="text-[10px] text-slate-400">Torque do Spindle</span>
                            <div class="text-xs font-mono font-bold text-purple-400">Estimado por kc</div>
                        </div>
                    </div>
                </div>

                <!-- Valores auxiliares compactos -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3 shrink-0">
                    <div class="bg-slate-800 p-3 rounded-lg border border-slate-700">
                        <span class="text-[11px] text-slate-400">Intercepção (a)</span>
                        <div class="font-mono text-sm font-bold text-white mt-0.5" id="val-a">0.1450 mm/rot</div>
                    </div>
                    <div class="bg-slate-800 p-3 rounded-lg border border-slate-700">
                        <span class="text-[11px] text-slate-400">Declive / Desvio (b)</span>
                        <div class="font-mono text-sm font-bold text-white mt-0.5" id="val-b">0.0300 mm/rot·mm</div>
                    </div>
                    <div class="bg-slate-800 p-3 rounded-lg border border-slate-700">
                        <span class="text-[11px] text-slate-400">Estado da Gama</span>
                        <div class="text-xs font-bold text-emerald-400 mt-1" id="val-estado">Dentro do intervalo consecutivo</div>
                    </div>
                </div>

                <!-- Tabela de Referência e Gráfico lado a lado -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 flex-1 min-h-[280px]">
                    <!-- Tabela de Referência -->
                    <div class="bg-slate-800 p-3.5 rounded-lg border border-slate-700 flex flex-col min-h-0">
                        <h3 class="text-[11px] font-semibold text-slate-400 uppercase mb-2 shrink-0">Tabela de Referência do Catálogo</h3>
                        <div class="overflow-y-auto flex-1 min-h-0 max-h-[220px]">
                            <table class="w-full text-left text-xs">
                                <thead class="sticky top-0 bg-slate-800">
                                    <tr class="border-b border-slate-700 text-slate-400">
                                        <th class="pb-1.5">Ø (mm)</th>
                                        <th class="pb-1.5">f Cat.</th>
                                        <th class="pb-1.5">RPM (n)</th>
                                        <th class="pb-1.5">Avanço (v_f)</th>
                                    </tr>
                                </thead>
                                <tbody id="tabela-ref" class="divide-y divide-slate-700/50"></tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Gráfico Interativo SVG -->
                    <div class="bg-slate-800 p-3.5 rounded-lg border border-slate-700 flex flex-col justify-between min-h-0">
                        <div class="flex justify-between items-center shrink-0">
                            <h3 class="text-[11px] font-semibold text-slate-400 uppercase">Curva por Intervalos: Avanço (f) vs. Ø</h3>
                            <span class="text-[9px] text-slate-400" id="badge-metodo">SVG Interativo</span>
                        </div>
                        <div class="relative w-full flex-1 bg-slate-900 rounded-md border border-slate-700 p-1 flex items-center justify-center my-2 min-h-[140px]">
                            <svg id="svg-grafico" class="w-full h-full max-h-40" viewBox="0 0 400 180" preserveAspectRatio="xMidYMid meet"></svg>
                        </div>
                        <div class="flex justify-center gap-4 text-[9px] text-slate-400 shrink-0">
                            <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-blue-500 inline-block"></span> Catálogo</span>
                            <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-orange-500 inline-block"></span> Calculado</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Assinatura / Rodapé Ultra-Compacto -->
        <footer class="bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/80 flex flex-col sm:flex-row justify-between items-center gap-2 text-[11px] text-slate-400 shrink-0">
            <div class="font-medium text-slate-300">
                Created by <span class="text-white font-semibold">Bruno Pinto</span>
            </div>
            <div class="flex flex-wrap items-center gap-4">
                <a href="mailto:bruno.pinto@alamo-ferramentas.com" class="hover:text-blue-400 transition flex items-center gap-1">
                    <span>✉️</span> bruno.pinto@alamo-ferramentas.com
                </a>
                <a href="tel:+351936959415" class="hover:text-blue-400 transition flex items-center gap-1">
                    <span>📱</span> +351 936 959 415
                </a>
            </div>
        </footer>
    </div>

    <script>
        let refrigAtual = 'int';
        let vcPct = 0;
        let fPct = 0;
        let fUnlocked = false;
        let vcUnlocked = false;
        let rpmMaxUnlocked = false;

        function toggleFullScreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(err => {
                    alert(`Erro ao tentar modo ecrã inteiro: ${err.message}`);
                });
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                }
            }
        }

        // Fatores aproximados de pressão específica de corte (kc) e densidades padrão (g/cm³) por grupo ISO
        const propriedadesGrupo = {
            'P': { kc: 2200, densidade: 7.85 },
            'M': { kc: 2800, densidade: 7.90 },
            'K': { kc: 1800, densidade: 7.20 },
            'N': { kc: 800,  densidade: 2.70 },
            'S': { kc: 3400, densidade: 4.50 },
            'H': { kc: 3200, densidade: 7.85 },
            'C': { kc: 1500, densidade: 1.60 }
        };

        function getKc(grupoKey) {
            const prefixo = grupoKey.charAt(0).toUpperCase();
            return propriedadesGrupo[prefixo] ? propriedadesGrupo[prefixo].kc : 2200;
        }

        function getDensidadePadrao(grupoKey) {
            const prefixo = grupoKey.charAt(0).toUpperCase();
            return propriedadesGrupo[prefixo] ? propriedadesGrupo[prefixo].densidade : 7.85;
        }

        const dados = {
            scd631: {
                linha: 'expert',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'Tritan-Drill-Uni-Plus SCD631',
                diametros: [4.00, 5.50, 7.50, 10.50, 14.50, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P5.1", "M1.1", "M1.2", "K1.1", "K2.1", "K2.2", "K2.3", "K3.1", "K3.2", "N1.1", "N1.2", "N1.3", "N1.4", "N2.1", "N2.2", "N2.3"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P5.1": "P5.1 — Aço fundido",
                    "M1.1": "M1.1 — Aços inoxidáveis austeníticos (< 700 N/mm²)",
                    "M1.2": "M1.2 — Aços inoxidáveis Duplex (< 1000 N/mm²)",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)",
                    "K3.1": "K3.1 — Ferro fundido GJV / Mableável GJM (< 500 N/mm²)",
                    "K3.2": "K3.2 — Ferro fundido GJV / Mableável GJM (> 500 N/mm²)",
                    "N1.1": "N1.1 — Alumínio não ligado e ligado < 3% Si",
                    "N1.2": "N1.2 — Alumínio ligado ≤ 7% Si",
                    "N1.3": "N1.3 — Alumínio ligado > 7-12% Si",
                    "N1.4": "N1.4 — Alumínio ligado > 12% Si",
                    "N2.1": "N2.1 — Cobre não ligado (< 300 N/mm²)",
                    "N2.2": "N2.2 — Cobre ligado (> 300 N/mm²)",
                    "N2.3": "N2.3 — Latão, bronze (< 1200 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {int:115, ext:105, mql:105, ar:0}, f: [0.22, 0.27, 0.34, 0.42, 0.51, 0.59] },
                    "P1.2": { vc: {int:105, ext:85, mql:85, ar:0}, f: [0.27, 0.34, 0.42, 0.53, 0.64, 0.74] },
                    "P2.1": { vc: {int:115, ext:100, mql:100, ar:0}, f: [0.25, 0.32, 0.40, 0.50, 0.60, 0.70] },
                    "P2.2": { vc: {int:80, ext:70, mql:70, ar:0}, f: [0.21, 0.26, 0.32, 0.40, 0.48, 0.55] },
                    "P3.1": { vc: {int:85, ext:75, mql:75, ar:0}, f: [0.23, 0.29, 0.36, 0.45, 0.54, 0.63] },
                    "P3.2": { vc: {int:70, ext:65, mql:65, ar:0}, f: [0.19, 0.24, 0.30, 0.37, 0.44, 0.51] },
                    "P3.3": { vc: {int:70, ext:50, mql:60, ar:0}, f: [0.16, 0.19, 0.29, 0.24, 0.34, 0.40] },
                    "P5.1": { vc: {int:115, ext:100, mql:100, ar:0}, f: [0.25, 0.32, 0.40, 0.50, 0.60, 0.70] },
                    "M1.1": { vc: {int:55, ext:35, mql:35, ar:0}, f: [0.11, 0.14, 0.18, 0.22, 0.27, 0.31] },
                    "M1.2": { vc: {int:140, ext:100, mql:100, ar:100}, f: [0.31, 0.41, 0.53, 0.68, 0.84, 0.98] },
                    "K1.1": { vc: {int:185, ext:140, mql:115, ar:140}, f: [0.30, 0.39, 0.50, 0.64, 0.78, 0.91] },
                    "K2.1": { vc: {int:115, ext:85, mql:85, ar:0}, f: [0.27, 0.35, 0.44, 0.55, 0.67, 0.78] },
                    "K2.2": { vc: {int:70, ext:45, mql:60, ar:0}, f: [0.14, 0.18, 0.28, 0.22, 0.33, 0.38] },
                    "K2.3": { vc: {int:105, ext:90, mql:90, ar:0}, f: [0.29, 0.37, 0.47, 0.59, 0.72, 0.84] },
                    "K3.1": { vc: {int:90, ext:80, mql:80, ar:0}, f: [0.25, 0.31, 0.48, 0.38, 0.57, 0.66] },
                    "K3.2": { vc: {int:345, ext:230, mql:290, ar:0}, f: [0.22, 0.27, 0.34, 0.42, 0.51, 0.59] },
                    "N1.1": { vc: {int:290, ext:205, mql:230, ar:0}, f: [0.27, 0.35, 0.55, 0.44, 0.67, 0.78] },
                    "N1.2": { vc: {int:255, ext:205, mql:175, ar:0}, f: [0.27, 0.35, 0.55, 0.44, 0.67, 0.78] },
                    "N1.3": { vc: {int:205, ext:175, mql:140, ar:0}, f: [0.27, 0.35, 0.55, 0.44, 0.67, 0.78] },
                    "N1.4": { vc: {int:140, ext:105, mql:0, ar:0}, f: [0.20, 0.26, 0.41, 0.33, 0.50, 0.58] },
                    "N2.1": { vc: {int:230, ext:185, mql:185, ar:140}, f: [0.31, 0.41, 0.68, 0.53, 0.84, 0.98] },
                    "N2.2": { vc: {int:230, ext:185, mql:185, ar:140}, f: [0.31, 0.41, 0.68, 0.53, 0.84, 0.98] },
                    "N2.3": { vc: {int:230, ext:185, mql:185, ar:140}, f: [0.31, 0.41, 0.68, 0.53, 0.84, 0.98] }
                }
            },
            scd221: {
                linha: 'expert',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'MEGA-Speed-Drill-Uni SCD221',
                diametros: [3.00, 4.50, 6.50, 9.50, 14.00, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P4.1", "P5.1", "P6.1", "K1.1", "K2.1", "K2.2", "K2.3", "K3.1", "K3.2"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P4.1": "P4.1 — Aços inoxidáveis ferríticos e martensíticos",
                    "P5.1": "P5.1 — Aço fundido",
                    "P6.1": "P6.1 — Aços fundidos inoxidáveis",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)",
                    "K3.1": "K3.1 — Ferro fundido GJV / Mableável GJM (< 500 N/mm²)",
                    "K3.2": "K3.2 — Ferro fundido GJV / Mableável GJM (> 500 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {int:170, ext:155, mql:155, ar:0}, f: [0.11, 0.14, 0.23, 0.18, 0.30, 0.36] },
                    "P1.2": { vc: {int:155, ext:130, mql:130, ar:0}, f: [0.14, 0.18, 0.22, 0.29, 0.37, 0.45] },
                    "P2.1": { vc: {int:170, ext:145, mql:145, ar:0}, f: [0.13, 0.17, 0.21, 0.27, 0.35, 0.43] },
                    "P2.2": { vc: {int:120, ext:100, mql:100, ar:0}, f: [0.11, 0.14, 0.17, 0.22, 0.28, 0.34] },
                    "P3.1": { vc: {int:130, ext:110, mql:110, ar:0}, f: [0.11, 0.15, 0.25, 0.19, 0.32, 0.38] },
                    "P3.2": { vc: {int:115, ext:100, mql:95, ar:0}, f: [0.10, 0.14, 0.22, 0.17, 0.28, 0.35] },
                    "P3.3": { vc: {int:100, ext:75, mql:85, ar:0}, f: [0.10, 0.13, 0.16, 0.20, 0.26, 0.31] },
                    "P4.1": { vc: {int:100, ext:75, mql:85, ar:0}, f: [0.08, 0.10, 0.16, 0.13, 0.21, 0.25] },
                    "P5.1": { vc: {int:170, ext:145, mql:145, ar:0}, f: [0.13, 0.17, 0.27, 0.21, 0.35, 0.43] },
                    "P6.1": { vc: {int:100, ext:85, mql:75, ar:0}, f: [0.08, 0.10, 0.13, 0.16, 0.21, 0.25] },
                    "K1.1": { vc: {int:150, ext:105, mql:105, ar:105}, f: [0.13, 0.19, 0.26, 0.35, 0.45, 0.54] },
                    "K2.1": { vc: {int:200, ext:150, mql:125, ar:150}, f: [0.13, 0.18, 0.25, 0.33, 0.42, 0.50] },
                    "K2.2": { vc: {int:125, ext:95, mql:95, ar:0}, f: [0.12, 0.16, 0.22, 0.28, 0.36, 0.43] },
                    "K2.3": { vc: {int:75, ext:50, mql:65, ar:0}, f: [0.09, 0.12, 0.15, 0.19, 0.24, 0.28] },
                    "K3.1": { vc: {int:115, ext:100, mql:100, ar:0}, f: [0.13, 0.18, 0.23, 0.31, 0.39, 0.46] },
                    "K3.2": { vc: {int:100, ext:90, mql:90, ar:0}, f: [0.11, 0.15, 0.19, 0.25, 0.31, 0.36] }
                }
            },
            scd231: {
                linha: 'expert',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'MEGA-180°-Drill SCD231',
                diametros: [3.00, 4.50, 6.50, 9.50, 14.00, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P5.1", "K1.1", "K2.1", "K2.2", "K2.3", "K3.1", "K3.2"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P5.1": "P5.1 — Aço fundido",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)",
                    "K3.1": "K3.1 — Ferro fundido GJV / Mableável GJM (< 500 N/mm²)",
                    "K3.2": "K3.2 — Ferro fundido GJV / Mableável GJM (> 500 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {int:80, ext:70, mql:70, ar:0}, f: [0.07, 0.09, 0.12, 0.16, 0.20, 0.24] },
                    "P1.2": { vc: {int:70, ext:60, mql:60, ar:0}, f: [0.09, 0.12, 0.15, 0.20, 0.25, 0.30] },
                    "P2.1": { vc: {int:80, ext:70, mql:70, ar:0}, f: [0.08, 0.11, 0.14, 0.19, 0.24, 0.28] },
                    "P2.2": { vc: {int:55, ext:50, mql:50, ar:0}, f: [0.07, 0.09, 0.12, 0.15, 0.19, 0.22] },
                    "P3.1": { vc: {int:60, ext:50, mql:50, ar:0}, f: [0.07, 0.10, 0.13, 0.17, 0.21, 0.25] },
                    "P3.2": { vc: {int:50, ext:45, mql:45, ar:0}, f: [0.06, 0.08, 0.11, 0.14, 0.17, 0.21] },
                    "P3.3": { vc: {int:50, ext:40, mql:35, ar:0}, f: [0.05, 0.07, 0.09, 0.11, 0.14, 0.16] },
                    "P5.1": { vc: {int:80, ext:70, mql:70, ar:0}, f: [0.08, 0.11, 0.14, 0.19, 0.24, 0.28] },
                    "K1.1": { vc: {int:95, ext:70, mql:70, ar:70}, f: [0.09, 0.14, 0.19, 0.25, 0.33, 0.39] },
                    "K2.1": { vc: {int:130, ext:95, mql:80, ar:95}, f: [0.10, 0.13, 0.18, 0.24, 0.30, 0.36] },
                    "K2.2": { vc: {int:80, ext:60, mql:60, ar:0}, f: [0.09, 0.12, 0.16, 0.21, 0.26, 0.31] },
                    "K2.3": { vc: {int:50, ext:40, mql:30, ar:0}, f: [0.06, 0.08, 0.11, 0.14, 0.17, 0.21] },
                    "K3.1": { vc: {int:70, ext:65, mql:65, ar:0}, f: [0.09, 0.13, 0.17, 0.22, 0.28, 0.33] },
                    "K3.2": { vc: {int:65, ext:55, mql:55, ar:0}, f: [0.08, 0.11, 0.14, 0.18, 0.22, 0.26] }
                }
            },
            scd241: {
                linha: 'expert',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'MEGA-180°-Drill-Alu SCD241 (Com Refrig. Interna)',
                diametros: [3.00, 4.50, 6.50, 9.50, 14.00, 20.00],
                gruposList: ["N1.1", "N1.2", "N1.3", "N1.4", "N2.1", "N2.2", "N2.3"],
                gruposNames: {
                    "N1.1": "N1.1 — Alumínio não ligado e ligado < 3% Si",
                    "N1.2": "N1.2 — Alumínio ligado ≤ 7% Si",
                    "N1.3": "N1.3 — Alumínio ligado > 7-12% Si",
                    "N1.4": "N1.4 — Alumínio ligado > 12% Si",
                    "N2.1": "N2.1 — Cobre não ligado e de baixa liga (< 300 N/mm²)",
                    "N2.2": "N2.2 — Cobre ligado (> 300 N/mm²)",
                    "N2.3": "N2.3 — Latão, bronze (< 1200 N/mm²)"
                },
                grupos: {
                    "N1.1": { vc: {int:240, ext:160, mql:200, ar:0}, f: [0.07, 0.09, 0.12, 0.16, 0.20, 0.24] },
                    "N1.2": { vc: {int:200, ext:145, mql:160, ar:0}, f: [0.09, 0.12, 0.16, 0.21, 0.26, 0.31] },
                    "N1.3": { vc: {int:175, ext:145, mql:120, ar:0}, f: [0.09, 0.12, 0.16, 0.21, 0.26, 0.31] },
                    "N1.4": { vc: {int:145, ext:95, mql:120, ar:0}, f: [0.09, 0.12, 0.16, 0.21, 0.26, 0.31] },
                    "N2.1": { vc: {int:110, ext:80, mql:0, ar:0}, f: [0.07, 0.09, 0.12, 0.16, 0.20, 0.24] },
                    "N2.2": { vc: {int:95, ext:70, mql:0, ar:0}, f: [0.09, 0.12, 0.16, 0.21, 0.26, 0.31] },
                    "N2.3": { vc: {int:160, ext:130, mql:130, ar:95}, f: [0.09, 0.14, 0.19, 0.25, 0.33, 0.39] }
                }
            },
            scd661: {
                linha: 'expert',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'SCD661 (Tritan-Drill-Steel)',
                diametros: [4.00, 5.50, 7.50, 10.50, 14.50, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "M1.1", "K1.1", "K2.1"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "M1.1": "M1.1 — Aços inoxidáveis austeníticos (< 700 N/mm²)",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {int:115, ext:105, mql:105, ar:100}, f: [0.24, 0.30, 0.37, 0.46, 0.56, 0.65] },
                    "P1.2": { vc: {int:105, ext:85, mql:85, ar:80}, f: [0.30, 0.37, 0.46, 0.58, 0.70, 0.81] },
                    "P2.1": { vc: {int:115, ext:100, mql:100, ar:90}, f: [0.28, 0.35, 0.44, 0.55, 0.66, 0.77] },
                    "P2.2": { vc: {int:80, ext:70, mql:70, ar:60}, f: [0.24, 0.29, 0.36, 0.44, 0.53, 0.61] },
                    "P3.1": { vc: {int:85, ext:75, mql:75, ar:70}, f: [0.25, 0.31, 0.39, 0.49, 0.60, 0.69] },
                    "P3.2": { vc: {int:70, ext:65, mql:65, ar:60}, f: [0.21, 0.26, 0.33, 0.41, 0.49, 0.56] },
                    "P3.3": { vc: {int:70, ext:50, mql:60, ar:45}, f: [0.18, 0.21, 0.26, 0.32, 0.38, 0.43] },
                    "M1.1": { vc: {int:55, ext:35, mql:35, ar:30}, f: [0.11, 0.14, 0.18, 0.22, 0.27, 0.31] },
                    "K1.1": { vc: {int:185, ext:115, mql:140, ar:100}, f: [0.34, 0.43, 0.55, 0.70, 0.85, 1.00] },
                    "K2.1": { vc: {int:115, ext:85, mql:85, ar:75}, f: [0.30, 0.38, 0.48, 0.61, 0.74, 0.86] }
                }
            },
            scd621: {
                linha: 'expert',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'SCD621 (MEGA-Speed-Drill-Steel)',
                diametros: [3.00, 4.50, 6.50, 9.50, 14.00, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "M1.1", "K1.1"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "M1.1": "M1.1 — Aços inoxidáveis austeníticos (< 700 N/mm²)",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {int:170, ext:155, mql:155, ar:150}, f: [0.13, 0.17, 0.22, 0.29, 0.36, 0.43] },
                    "P1.2": { vc: {int:155, ext:130, mql:130, ar:120}, f: [0.16, 0.21, 0.28, 0.36, 0.45, 0.54] },
                    "P2.1": { vc: {int:170, ext:145, mql:145, ar:130}, f: [0.15, 0.20, 0.26, 0.34, 0.43, 0.51] },
                    "P2.2": { vc: {int:120, ext:100, mql:100, ar:90}, f: [0.13, 0.17, 0.21, 0.27, 0.34, 0.40] },
                    "P3.1": { vc: {int:130, ext:110, mql:110, ar:100}, f: [0.13, 0.18, 0.23, 0.30, 0.39, 0.46] },
                    "P3.2": { vc: {int:100, ext:95, mql:95, ar:85}, f: [0.12, 0.15, 0.20, 0.25, 0.32, 0.37] },
                    "P3.3": { vc: {int:100, ext:75, mql:85, ar:70}, f: [0.10, 0.12, 0.16, 0.20, 0.25, 0.29] },
                    "M1.1": { vc: {int:65, ext:40, mql:40, ar:35}, f: [0.07, 0.09, 0.12, 0.15, 0.19, 0.23] },
                    "K1.1": { vc: {int:150, ext:105, mql:105, ar:95}, f: [0.14, 0.21, 0.28, 0.38, 0.49, 0.59] }
                }
            },
            scd411: {
                linha: 'expert',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'MEGA-Speed-Drill-Inox SCD411 (Com Refrig. Interna)',
                diametros: [3.00, 4.50, 6.50, 9.50, 14.00, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P4.1", "P5.1", "P6.1", "M1.1", "M1.2", "M2.1", "M3.1", "S1.1", "S2.1", "S2.2", "S3.1", "S3.2", "S4.1", "S5.1"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P4.1": "P4.1 — Aços inoxidáveis ferríticos e martensíticos",
                    "P5.1": "P5.1 — Aço fundido",
                    "P6.1": "P6.1 — Aços fundidos inoxidáveis ferríticos/martensíticos",
                    "M1.1": "M1.1 — Aços inoxidáveis austeníticos (< 700 N/mm²)",
                    "M1.2": "M1.2 — Aços inoxidáveis Duplex (< 1000 N/mm²)",
                    "M2.1": "M2.1 — Aços fundidos austeníticos (< 700 N/mm²)",
                    "M3.1": "M3.1 — Aços fundidos Duplex (< 1000 N/mm²)",
                    "S1.1": "S1.1 — Titânio e ligas de titânio (< 400 N/mm²)",
                    "S2.1": "S2.1 — Titânio e ligas de titânio (< 1200 N/mm²)",
                    "S2.2": "S2.2 — Titânio e ligas de titânio (> 1200 N/mm²)",
                    "S3.1": "S3.1 — Níquel não ligado e ligado (< 900 N/mm²)",
                    "S3.2": "S3.2 — Níquel não ligado e ligado (> 900 N/mm²)",
                    "S4.1": "S4.1 — Superligas de alta temperatura (Ni, Co, Fe)",
                    "S5.1": "S5.1 — Ligas de tungsténio e molibdénio"
                },
                grupos: {
                    "P1.1": { vc: {int:150, ext:135, mql:135, ar:0}, f: [0.09, 0.12, 0.15, 0.20, 0.25, 0.30] },
                    "P1.2": { vc: {int:135, ext:115, mql:115, ar:0}, f: [0.11, 0.15, 0.19, 0.25, 0.31, 0.37] },
                    "P2.1": { vc: {int:150, ext:130, mql:130, ar:0}, f: [0.10, 0.14, 0.18, 0.23, 0.30, 0.35] },
                    "P2.2": { vc: {int:105, ext:90, mql:90, ar:0}, f: [0.09, 0.12, 0.15, 0.19, 0.24, 0.28] },
                    "P3.1": { vc: {int:115, ext:100, mql:100, ar:0}, f: [0.09, 0.12, 0.16, 0.21, 0.27, 0.32] },
                    "P3.2": { vc: {int:90, ext:85, mql:85, ar:0}, f: [0.08, 0.10, 0.13, 0.17, 0.22, 0.26] },
                    "P3.3": { vc: {int:90, ext:70, mql:75, ar:0}, f: [0.07, 0.09, 0.11, 0.14, 0.17, 0.20] },
                    "P4.1": { vc: {int:70, ext:55, mql:60, ar:0}, f: [0.06, 0.08, 0.11, 0.14, 0.18, 0.21] },
                    "P5.1": { vc: {int:150, ext:130, mql:130, ar:0}, f: [0.10, 0.14, 0.18, 0.23, 0.30, 0.35] },
                    "P6.1": { vc: {int:70, ext:60, mql:55, ar:0}, f: [0.06, 0.08, 0.11, 0.14, 0.18, 0.21] },
                    "M1.1": { vc: {int:80, ext:50, mql:50, ar:0}, f: [0.08, 0.10, 0.13, 0.17, 0.22, 0.26] },
                    "M1.2": { vc: {int:75, ext:45, mql:45, ar:0}, f: [0.07, 0.09, 0.11, 0.15, 0.19, 0.22] },
                    "M2.1": { vc: {int:80, ext:50, mql:50, ar:0}, f: [0.08, 0.10, 0.13, 0.17, 0.22, 0.26] },
                    "M3.1": { vc: {int:75, ext:45, mql:45, ar:0}, f: [0.07, 0.09, 0.11, 0.15, 0.19, 0.22] },
                    "S1.1": { vc: {int:35, ext:25, mql:25, ar:0}, f: [0.06, 0.08, 0.11, 0.14, 0.18, 0.21] },
                    "S2.1": { vc: {int:30, ext:20, mql:20, ar:0}, f: [0.05, 0.07, 0.09, 0.12, 0.15, 0.18] },
                    "S2.2": { vc: {int:25, ext:20, mql:20, ar:0}, f: [0.04, 0.06, 0.07, 0.10, 0.12, 0.14] },
                    "S3.1": { vc: {int:20, ext:10, mql:10, ar:0}, f: [0.05, 0.07, 0.09, 0.12, 0.15, 0.18] },
                    "S3.2": { vc: {int:20, ext:10, mql:10, ar:0}, f: [0.04, 0.06, 0.07, 0.10, 0.12, 0.14] },
                    "S4.1": { vc: {int:20, ext:10, mql:10, ar:0}, f: [0.04, 0.06, 0.07, 0.10, 0.12, 0.14] },
                    "S5.1": { vc: {int:0, ext:0, mql:0, ar:0}, f: [0.07, 0.10, 0.13, 0.17, 0.21, 0.25] }
                }
            },
            scd421: {
                linha: 'expert',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'MEGA-Speed-Drill-Iron SCD421 (Com Refrig. Interna)',
                diametros: [3.00, 4.50, 6.50, 9.50, 14.00, 20.00],
                gruposList: ["K1.1", "K2.1", "K2.2", "K2.3", "K3.1", "K3.2"],
                gruposNames: {
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)",
                    "K3.1": "K3.1 — Ferro fundido GJV / Mableável GJM (< 500 N/mm²)",
                    "K3.2": "K3.2 — Ferro fundido GJV / Mableável GJM (> 500 N/mm²)"
                },
                grupos: {
                    "K1.1": { vc: {int:170, ext:120, mql:120, ar:120}, f: [0.15, 0.21, 0.29, 0.40, 0.51, 0.61] },
                    "K2.1": { vc: {int:225, ext:170, mql:170, ar:140}, f: [0.15, 0.21, 0.28, 0.37, 0.48, 0.57] },
                    "K2.2": { vc: {int:140, ext:105, mql:105, ar:105}, f: [0.14, 0.19, 0.32, 0.25, 0.41, 0.49] },
                    "K2.3": { vc: {int:85, ext:55, mql:70, ar:0}, f: [0.10, 0.13, 0.17, 0.22, 0.27, 0.32] },
                    "K3.1": { vc: {int:125, ext:110, mql:110, ar:0}, f: [0.15, 0.20, 0.35, 0.26, 0.44, 0.52] },
                    "K3.2": { vc: {int:110, ext:100, mql:100, ar:0}, f: [0.13, 0.17, 0.22, 0.28, 0.35, 0.41] }
                }
            },
            scd271: {
                linha: 'expert',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'MEGA-Drill-Composite-UDX SCD271 (Com Refrig. Interna)',
                diametros: [3.00, 4.00, 5.50, 7.50, 10.00, 12.00],
                gruposList: ["C1.1", "C1.2", "C1.3", "C2.1"],
                gruposNames: {
                    "C1.1": "C1.1 — Matriz plástica, reforçada com fibra de aramida (AFRP)",
                    "C1.2": "C1.2 — Matriz plástica (termofixa), CFRP / GFRP",
                    "C1.3": "C1.3 — Matriz plástica (termoplástica), CFRP / GFRP",
                    "C2.1": "C2.1 — Matriz de carbono, reforçada com fibra de carbono (CFC)"
                },
                grupos: {
                    "C1.1": { vc: {int:90, ext:75, mql:75, ar:75}, f: [0.04, 0.04, 0.06, 0.05, 0.07, 0.08] },
                    "C1.2": { vc: {int:75, ext:75, mql:75, ar:75}, f: [0.04, 0.04, 0.06, 0.05, 0.07, 0.08] },
                    "C1.3": { vc: {int:75, ext:75, mql:75, ar:75}, f: [0.04, 0.04, 0.06, 0.05, 0.07, 0.08] },
                    "C2.1": { vc: {int:90, ext:75, mql:75, ar:75}, f: [0.04, 0.04, 0.06, 0.05, 0.07, 0.08] }
                }
            },
            scd600: {
                linha: 'performance',
                categoria: 'solid',
                temRefrigInt: false,
                nome: 'MEGA-Drill-Steel-Plus SCD600 (Sem Refrig. Interna)',
                diametros: [3.00, 4.50, 6.50, 9.50, 14.00, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P4.1", "P5.1", "P6.1", "K1.1", "K2.1", "K2.2", "K2.3", "K3.1", "K3.2", "H1.1", "H1.2"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P4.1": "P4.1 — Aços inoxidáveis ferríticos e martensíticos",
                    "P5.1": "P5.1 — Aço fundido",
                    "P6.1": "P6.1 — Aços fundidos inoxidáveis ferríticos e martensíticos",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)",
                    "K3.1": "K3.1 — Ferro fundido esferoidal GJV / Mableável GJM (< 500 N/mm²)",
                    "K3.2": "K3.2 — Ferro fundido esferoidal GJV / Mableável GJM (> 500 N/mm²)",
                    "H1.1": "H1.1 — Aços temperados / Aço fundido (< 44 HRC)",
                    "H1.2": "H1.2 — Aços temperados / Aço fundido (< 55 HRC)"
                },
                grupos: {
                    "P1.1": { vc: {ext:100, mql:100, ar:0}, f: [0.10, 0.13, 0.17, 0.22, 0.28, 0.33] },
                    "P1.2": { vc: {ext:85, mql:85, ar:0}, f: [0.12, 0.16, 0.21, 0.27, 0.34, 0.41] },
                    "P2.1": { vc: {ext:95, mql:95, ar:0}, f: [0.11, 0.15, 0.20, 0.26, 0.33, 0.38] },
                    "P2.2": { vc: {ext:65, mql:65, ar:0}, f: [0.10, 0.13, 0.16, 0.21, 0.26, 0.30] },
                    "P3.1": { vc: {ext:70, mql:70, ar:0}, f: [0.10, 0.14, 0.18, 0.23, 0.29, 0.35] },
                    "P3.2": { vc: {ext:60, mql:60, ar:0}, f: [0.09, 0.12, 0.15, 0.19, 0.24, 0.28] },
                    "P3.3": { vc: {ext:50, mql:55, ar:0}, f: [0.07, 0.09, 0.12, 0.15, 0.19, 0.22] },
                    "P4.1": { vc: {ext:50, mql:55, ar:0}, f: [0.07, 0.09, 0.12, 0.15, 0.19, 0.23] },
                    "P5.1": { vc: {ext:95, mql:95, ar:0}, f: [0.11, 0.15, 0.20, 0.26, 0.33, 0.38] },
                    "P6.1": { vc: {ext:50, mql:55, ar:0}, f: [0.07, 0.09, 0.12, 0.15, 0.19, 0.23] },
                    "K1.1": { vc: {ext:85, mql:85, ar:85}, f: [0.13, 0.19, 0.26, 0.35, 0.45, 0.54] },
                    "K2.1": { vc: {ext:100, mql:120, ar:120}, f: [0.13, 0.18, 0.25, 0.33, 0.42, 0.50] },
                    "K2.2": { vc: {ext:75, mql:75, ar:0}, f: [0.12, 0.16, 0.22, 0.28, 0.36, 0.43] },
                    "K2.3": { vc: {ext:40, mql:50, ar:0}, f: [0.09, 0.12, 0.15, 0.19, 0.24, 0.28] },
                    "K3.1": { vc: {ext:80, mql:80, ar:0}, f: [0.13, 0.18, 0.23, 0.31, 0.39, 0.46] },
                    "K3.2": { vc: {ext:70, mql:70, ar:0}, f: [0.11, 0.15, 0.19, 0.25, 0.31, 0.36] },
                    "H1.1": { vc: {ext:90, mql:90, ar:0}, f: [0.09, 0.12, 0.15, 0.19, 0.24, 0.28] },
                    "H1.2": { vc: {ext:25, mql:25, ar:0}, f: [0.05, 0.06, 0.08, 0.11, 0.14, 0.16] }
                }
            },
            scd601: {
                linha: 'performance',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'MEGA-Drill-Steel-Plus SCD601 (Com Refrig. Interna)',
                diametros: [3.00, 4.50, 6.50, 9.50, 14.00, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P4.1", "P5.1", "P6.1", "K1.1", "K2.1", "K2.2", "K2.3", "K3.1", "K3.2", "H1.1", "H1.2"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P4.1": "P4.1 — Aços inoxidáveis ferríticos e martensíticos",
                    "P5.1": "P5.1 — Aço fundido",
                    "P6.1": "P6.1 — Aços fundidos inoxidáveis ferríticos e martensíticos",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)",
                    "K3.1": "K3.1 — Ferro fundido esferoidal GJV / Mableável GJM (< 500 N/mm²)",
                    "K3.2": "K3.2 — Ferro fundido esferoidal GJV / Mableável GJM (> 500 N/mm²)",
                    "H1.1": "H1.1 — Aços temperados / Aço fundido (< 44 HRC)",
                    "H1.2": "H1.2 — Aços temperados / Aço fundido (< 55 HRC)"
                },
                grupos: {
                    "P1.1": { vc: {int:110, ext:100, mql:100, ar:0}, f: [0.10, 0.13, 0.17, 0.22, 0.28, 0.33] },
                    "P1.2": { vc: {int:100, ext:85, mql:85, ar:0}, f: [0.12, 0.16, 0.21, 0.27, 0.34, 0.41] },
                    "P2.1": { vc: {int:110, ext:95, mql:95, ar:0}, f: [0.11, 0.15, 0.20, 0.26, 0.33, 0.38] },
                    "P2.2": { vc: {int:75, ext:65, mql:65, ar:0}, f: [0.10, 0.13, 0.16, 0.21, 0.26, 0.30] },
                    "P3.1": { vc: {int:85, ext:70, mql:70, ar:0}, f: [0.10, 0.14, 0.18, 0.23, 0.29, 0.35] },
                    "P3.2": { vc: {int:65, ext:60, mql:60, ar:0}, f: [0.09, 0.12, 0.15, 0.19, 0.24, 0.28] },
                    "P3.3": { vc: {int:65, ext:50, mql:55, ar:0}, f: [0.07, 0.09, 0.12, 0.15, 0.19, 0.22] },
                    "P4.1": { vc: {int:65, ext:50, mql:55, ar:0}, f: [0.07, 0.09, 0.12, 0.15, 0.19, 0.23] },
                    "P5.1": { vc: {int:110, ext:95, mql:95, ar:0}, f: [0.11, 0.15, 0.20, 0.26, 0.33, 0.38] },
                    "P6.1": { vc: {int:65, ext:50, mql:55, ar:0}, f: [0.07, 0.09, 0.12, 0.15, 0.19, 0.23] },
                    "K1.1": { vc: {int:120, ext:85, mql:85, ar:85}, f: [0.13, 0.19, 0.26, 0.35, 0.45, 0.54] },
                    "K2.1": { vc: {int:160, ext:100, mql:120, ar:120}, f: [0.13, 0.18, 0.25, 0.33, 0.42, 0.50] },
                    "K2.2": { vc: {int:100, ext:75, mql:75, ar:0}, f: [0.12, 0.16, 0.22, 0.28, 0.36, 0.43] },
                    "K2.3": { vc: {int:60, ext:40, mql:50, ar:0}, f: [0.09, 0.12, 0.15, 0.19, 0.24, 0.28] },
                    "K3.1": { vc: {int:90, ext:80, mql:80, ar:0}, f: [0.13, 0.18, 0.23, 0.31, 0.39, 0.46] },
                    "K3.2": { vc: {int:80, ext:70, mql:70, ar:0}, f: [0.11, 0.15, 0.19, 0.25, 0.31, 0.36] },
                    "H1.1": { vc: {int:90, ext:90, mql:90, ar:0}, f: [0.09, 0.12, 0.15, 0.19, 0.24, 0.28] },
                    "H1.2": { vc: {int:25, ext:25, mql:25, ar:0}, f: [0.05, 0.06, 0.08, 0.11, 0.14, 0.16] }
                }
            },
            scd610: {
                linha: 'performance',
                categoria: 'solid',
                temRefrigInt: false,
                nome: 'MEGA-Quadro-Drill-Plus SCD610 (Sem Refrig. Interna)',
                diametros: [4.00, 5.50, 7.50, 10.50, 14.50, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P5.1", "K1.1", "K2.1", "K2.2", "K2.3", "K3.1", "K3.2"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P5.1": "P5.1 — Aço fundido",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)",
                    "K3.1": "K3.1 — Ferro fundido GJV / Mableável GJM (< 500 N/mm²)",
                    "K3.2": "K3.2 — Ferro fundido GJV / Mableável GJM (> 500 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {ext:100, mql:100, ar:0}, f: [0.10, 0.13, 0.17, 0.22, 0.28, 0.33] },
                    "P1.2": { vc: {ext:85, mql:85, ar:0}, f: [0.12, 0.16, 0.27, 0.21, 0.34, 0.41] },
                    "P2.1": { vc: {ext:95, mql:95, ar:0}, f: [0.11, 0.15, 0.26, 0.20, 0.33, 0.38] },
                    "P2.2": { vc: {ext:65, mql:65, ar:0}, f: [0.10, 0.13, 0.21, 0.16, 0.26, 0.30] },
                    "P3.1": { vc: {ext:70, mql:70, ar:0}, f: [0.10, 0.14, 0.18, 0.23, 0.29, 0.35] },
                    "P3.2": { vc: {ext:60, mql:60, ar:0}, f: [0.09, 0.12, 0.19, 0.15, 0.24, 0.28] },
                    "P3.3": { vc: {ext:50, mql:55, ar:0}, f: [0.07, 0.09, 0.12, 0.15, 0.19, 0.22] },
                    "P5.1": { vc: {ext:95, mql:95, ar:0}, f: [0.11, 0.15, 0.26, 0.20, 0.33, 0.38] },
                    "K1.1": { vc: {ext:95, mql:95, ar:95}, f: [0.13, 0.19, 0.35, 0.26, 0.45, 0.54] },
                    "K2.1": { vc: {ext:110, mql:130, ar:130}, f: [0.13, 0.18, 0.25, 0.33, 0.42, 0.50] },
                    "K2.2": { vc: {ext:85, mql:85, ar:0}, f: [0.12, 0.16, 0.28, 0.22, 0.36, 0.43] },
                    "K2.3": { vc: {ext:45, mql:55, ar:0}, f: [0.09, 0.12, 0.19, 0.15, 0.24, 0.28] },
                    "K3.1": { vc: {ext:90, mql:90, ar:0}, f: [0.13, 0.18, 0.23, 0.31, 0.39, 0.46] },
                    "K3.2": { vc: {ext:75, mql:75, ar:0}, f: [0.11, 0.15, 0.19, 0.25, 0.31, 0.36] }
                }
            },
            scd611: {
                linha: 'performance',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'MEGA-Quadro-Drill-Plus SCD611 (Com Refrig. Interna)',
                diametros: [4.00, 5.50, 7.50, 10.50, 14.50, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P5.1", "K1.1", "K2.1", "K2.2", "K2.3", "K3.1", "K3.2"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P5.1": "P5.1 — Aço fundido",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)",
                    "K3.1": "K3.1 — Ferro fundido GJV / Mableável GJM (< 500 N/mm²)",
                    "K3.2": "K3.2 — Ferro fundido GJV / Mableável GJM (> 500 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {int:110, ext:100, mql:100, ar:0}, f: [0.10, 0.13, 0.17, 0.22, 0.28, 0.33] },
                    "P1.2": { vc: {int:100, ext:85, mql:85, ar:0}, f: [0.12, 0.16, 0.27, 0.21, 0.34, 0.41] },
                    "P2.1": { vc: {int:110, ext:95, mql:95, ar:0}, f: [0.11, 0.15, 0.26, 0.20, 0.33, 0.38] },
                    "P2.2": { vc: {int:75, ext:65, mql:65, ar:0}, f: [0.10, 0.13, 0.21, 0.16, 0.26, 0.30] },
                    "P3.1": { vc: {int:85, ext:70, mql:70, ar:0}, f: [0.10, 0.14, 0.18, 0.23, 0.29, 0.35] },
                    "P3.2": { vc: {int:65, ext:60, mql:60, ar:0}, f: [0.09, 0.12, 0.19, 0.15, 0.24, 0.28] },
                    "P3.3": { vc: {int:65, ext:50, mql:55, ar:0}, f: [0.07, 0.09, 0.12, 0.15, 0.19, 0.22] },
                    "P5.1": { vc: {int:110, ext:95, mql:95, ar:0}, f: [0.11, 0.15, 0.26, 0.20, 0.33, 0.38] },
                    "K1.1": { vc: {int:130, ext:95, mql:95, ar:95}, f: [0.13, 0.19, 0.35, 0.26, 0.45, 0.54] },
                    "K2.1": { vc: {int:175, ext:110, mql:130, ar:130}, f: [0.13, 0.18, 0.25, 0.33, 0.42, 0.50] },
                    "K2.2": { vc: {int:110, ext:85, mql:85, ar:0}, f: [0.12, 0.16, 0.28, 0.22, 0.36, 0.43] },
                    "K2.3": { vc: {int:65, ext:45, mql:55, ar:0}, f: [0.09, 0.12, 0.19, 0.15, 0.24, 0.28] },
                    "K3.1": { vc: {int:100, ext:90, mql:90, ar:0}, f: [0.13, 0.18, 0.23, 0.31, 0.39, 0.46] },
                    "K3.2": { vc: {int:90, ext:75, mql:75, ar:0}, f: [0.11, 0.15, 0.19, 0.25, 0.31, 0.36] }
                }
            },
            scd371: {
                linha: 'performance',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'MICRO-Drill-Steel SCD371 (Com Refrig. Interna)',
                diametros: [4.00, 5.50, 7.50, 10.50, 14.50, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P5.1", "M1.1", "M1.2", "K1.1", "K2.1", "K2.2", "K2.3", "K3.1", "K3.2"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P5.1": "P5.1 — Aço fundido",
                    "M1.1": "M1.1 — Aços inoxidáveis austeníticos (< 700 N/mm²)",
                    "M1.2": "M1.2 — Aços inoxidáveis Duplex (< 1000 N/mm²)",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)",
                    "K3.1": "K3.1 — Ferro fundido GJV / Mableável GJM (< 500 N/mm²)",
                    "K3.2": "K3.2 — Ferro fundido GJV / Mableável GJM (> 500 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {int:80, ext:70, mql:70, ar:0}, f: [0.04, 0.04, 0.05, 0.06, 0.07, 0.08] },
                    "P1.2": { vc: {int:70, ext:60, mql:60, ar:0}, f: [0.04, 0.05, 0.07, 0.06, 0.08, 0.10] },
                    "P2.1": { vc: {int:80, ext:70, mql:70, ar:0}, f: [0.04, 0.05, 0.06, 0.07, 0.08, 0.09] },
                    "P2.2": { vc: {int:55, ext:50, mql:50, ar:0}, f: [0.04, 0.05, 0.05, 0.06, 0.07, 0.08] },
                    "P3.1": { vc: {int:60, ext:50, mql:50, ar:0}, f: [0.04, 0.04, 0.05, 0.06, 0.07, 0.08] },
                    "P3.2": { vc: {int:50, ext:45, mql:45, ar:0}, f: [0.04, 0.04, 0.05, 0.04, 0.06, 0.07] },
                    "P3.3": { vc: {int:50, ext:35, mql:40, ar:0}, f: [0.03, 0.04, 0.05, 0.04, 0.05, 0.06] },
                    "P5.1": { vc: {int:80, ext:70, mql:70, ar:0}, f: [0.04, 0.05, 0.07, 0.06, 0.08, 0.09] },
                    "M1.1": { vc: {int:40, ext:25, mql:25, ar:0}, f: [0.03, 0.03, 0.04, 0.03, 0.05, 0.06] },
                    "M1.2": { vc: {int:95, ext:70, mql:70, ar:70}, f: [0.03, 0.04, 0.06, 0.05, 0.08, 0.11] },
                    "K1.1": { vc: {int:130, ext:80, mql:95, ar:95}, f: [0.04, 0.05, 0.07, 0.06, 0.09, 0.11] },
                    "K2.1": { vc: {int:80, ext:60, mql:60, ar:0}, f: [0.04, 0.05, 0.05, 0.07, 0.08, 0.10] },
                    "K2.2": { vc: {int:70, ext:65, mql:65, ar:0}, f: [0.04, 0.05, 0.07, 0.06, 0.09, 0.11] },
                    "K2.3": { vc: {int:65, ext:55, mql:55, ar:0}, f: [0.04, 0.05, 0.07, 0.06, 0.08, 0.09] },
                    "K3.1": { vc: {int:55, ext:45, mql:45, ar:0}, f: [0.04, 0.04, 0.05, 0.06, 0.07, 0.08] },
                    "K3.2": { vc: {int:45, ext:40, mql:40, ar:0}, f: [0.03, 0.04, 0.05, 0.04, 0.06, 0.07] }
                }
            },
            scd140: {
                linha: 'performance',
                categoria: 'solid',
                temRefrigInt: false,
                nome: 'MEGA-Drill-Hardened SCD140 (Sem Refrig. Interna)',
                diametros: [2.50, 3.62, 5.25, 7.61, 11.04, 16.00],
                gruposList: ["H1.1", "H1.2", "H2.1", "H2.2", "H2.3"],
                gruposNames: {
                    "H1.1": "H1.1 — Aço temperado / Aço fundido (< 44 HRC)",
                    "H1.2": "H1.2 — Aço temperado / Aço fundido (< 55 HRC)",
                    "H2.1": "H2.1 — Aço temperado / Aço fundido (< 60 HRC)",
                    "H2.2": "H2.2 — Aço temperado / Aço fundido (< 65 HRC)",
                    "H2.3": "H2.3 — Aço temperado / Aço fundido (< 68 HRC)"
                },
                grupos: {
                    "H1.1": { vc: {ext:80, mql:80, ar:0}, f: [0.07, 0.09, 0.11, 0.02, 0.19, 0.20] },
                    "H1.2": { vc: {ext:30, mql:30, ar:0}, f: [0.05, 0.06, 0.10, 0.08, 0.13, 0.16] },
                    "H2.1": { vc: {ext:30, mql:30, ar:0}, f: [0.04, 0.05, 0.09, 0.07, 0.11, 0.13] },
                    "H2.2": { vc: {ext:20, mql:20, ar:0}, f: [0.03, 0.04, 0.05, 0.06, 0.08, 0.09] },
                    "H2.3": { vc: {ext:15, mql:15, ar:0}, f: [0.03, 0.04, 0.05, 0.06, 0.08, 0.09] }
                }
            },
            scd131: {
                linha: 'performance',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'MEGA-Drill-Alu SCD131 (Com Refrig. Interna)',
                diametros: [3.00, 4.50, 6.50, 9.50, 14.00, 20.00],
                gruposList: ["N1.1", "N1.2", "N1.3", "N1.4", "N2.1", "N2.2", "N2.3"],
                gruposNames: {
                    "N1.1": "N1.1 — Alumínio não ligado e ligado < 3% Si",
                    "N1.2": "N1.2 — Alumínio ligado ≤ 7% Si",
                    "N1.3": "N1.3 — Alumínio ligado > 7-12% Si",
                    "N1.4": "N1.4 — Alumínio ligado > 12% Si",
                    "N2.1": "N2.1 — Cobre não ligado (< 300 N/mm²)",
                    "N2.2": "N2.2 — Cobre ligado (> 300 N/mm²)",
                    "N2.3": "N2.3 — Latão, bronze (< 1200 N/mm²)"
                },
                grupos: {
                    "N1.1": { vc: {int:300, ext:200, mql:250, ar:200}, f: [0.09, 0.12, 0.15, 0.20, 0.25, 0.30] },
                    "N1.2": { vc: {int:250, ext:180, mql:200, ar:160}, f: [0.11, 0.15, 0.20, 0.26, 0.33, 0.39] },
                    "N1.3": { vc: {int:220, ext:150, mql:180, ar:160}, f: [0.11, 0.15, 0.20, 0.26, 0.33, 0.39] },
                    "N1.4": { vc: {int:180, ext:120, mql:150, ar:120}, f: [0.11, 0.15, 0.20, 0.26, 0.33, 0.39] },
                    "N2.1": { vc: {int:140, ext:100, mql:120, ar:0}, f: [0.09, 0.12, 0.15, 0.20, 0.25, 0.30] },
                    "N2.2": { vc: {int:120, ext:90, mql:100, ar:0}, f: [0.11, 0.15, 0.26, 0.20, 0.33, 0.39] },
                    "N2.3": { vc: {int:200, ext:160, mql:160, ar:0}, f: [0.09, 0.14, 0.19, 0.25, 0.33, 0.39] }
                }
            },
            scd250: {
                linha: 'performance',
                categoria: 'solid',
                temRefrigInt: false,
                nome: 'MEGA-Drill-Composite-MD SCD250 (Sem Refrig. Interna)',
                diametros: [3.00, 4.00, 5.50, 7.50, 10.00, 12.00],
                gruposList: ["N3.1", "N3.2", "C1.1", "C1.2", "C1.3", "C2.1", "C3.1"],
                gruposNames: {
                    "N3.1": "N3.1 — Grafite, > 8 µm",
                    "N3.2": "N3.2 — Grafite, ≤ 8 µm",
                    "C1.1": "C1.1 — Matriz plástica, reforçada com fibra de aramida (AFRP)",
                    "C1.2": "C1.2 — Matriz plástica (termofixa), CFRP / GFRP",
                    "C1.3": "C1.3 — Matriz plástica (termoplástica), CFRP / GFRP",
                    "C2.1": "C2.1 — Matriz de carbono, reforçada com fibra de carbono (CFC)",
                    "C3.1": "C3.1 — Matriz metálica (MMC)"
                },
                grupos: {
                    "N3.1": { vc: {ext:200, mql:200, ar:200}, f: [0.07, 0.09, 0.11, 0.14, 0.16, 0.18] },
                    "N3.2": { vc: {ext:200, mql:200, ar:200}, f: [0.07, 0.09, 0.11, 0.14, 0.16, 0.18] },
                    "C1.1": { vc: {ext:90, mql:90, ar:90}, f: [0.04, 0.04, 0.05, 0.06, 0.07, 0.08] },
                    "C1.2": { vc: {ext:75, mql:75, ar:75}, f: [0.04, 0.04, 0.05, 0.06, 0.07, 0.08] },
                    "C1.3": { vc: {ext:75, mql:75, ar:75}, f: [0.04, 0.04, 0.05, 0.06, 0.07, 0.08] },
                    "C2.1": { vc: {ext:400, mql:400, ar:400}, f: [0.04, 0.04, 0.05, 0.06, 0.07, 0.08] },
                    "C3.1": { vc: {ext:400, mql:400, ar:400}, f: [0.04, 0.04, 0.05, 0.06, 0.07, 0.08] }
                }
            },
            scd270: {
                linha: 'expert',
                categoria: 'solid',
                temRefrigInt: false,
                nome: 'MEGA-Drill-Composite-UDX SCD270 (Sem Refrig. Interna)',
                diametros: [3.00, 4.00, 5.50, 7.50, 10.00, 12.00],
                gruposList: ["C1.1", "C1.2", "C1.3", "C2.1"],
                gruposNames: {
                    "C1.1": "C1.1 — Matriz plástica, reforçada com fibra de aramida (AFRP)",
                    "C1.2": "C1.2 — Matriz plástica (termofixa), CFRP / GFRP",
                    "C1.3": "C1.3 — Matriz plástica (termoplástica), CFRP / GFRP",
                    "C2.1": "C2.1 — Matriz de carbono, reforçada com fibra de carbono (CFC)"
                },
                grupos: {
                    "C1.1": { vc: {ext:90, mql:90, ar:90}, f: [0.04, 0.04, 0.06, 0.05, 0.07, 0.08] },
                    "C1.2": { vc: {ext:75, mql:75, ar:75}, f: [0.04, 0.04, 0.06, 0.05, 0.07, 0.08] },
                    "C1.3": { vc: {ext:75, mql:75, ar:75}, f: [0.04, 0.04, 0.06, 0.05, 0.07, 0.08] },
                    "C2.1": { vc: {ext:75, mql:75, ar:75}, f: [0.04, 0.04, 0.06, 0.05, 0.07, 0.08] }
                }
            },
            scd120: {
                linha: 'performance',
                categoria: 'solid',
                temRefrigInt: false,
                nome: 'MEGA-Drill-Inox SCD120 (Sem Refrig. Interna)',
                diametros: [3.00, 4.50, 6.50, 9.50, 14.00, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P4.1", "P5.1", "P6.1", "M1.1", "M1.2", "M2.1", "M3.1", "K1.1", "K2.1", "K2.2", "K2.3", "K3.1", "K3.2", "N2.1", "N2.2", "N2.3"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P4.1": "P4.1 — Aços inoxidáveis ferríticos e martensíticos",
                    "P5.1": "P5.1 — Aço fundido",
                    "P6.1": "P6.1 — Aços fundidos inoxidáveis",
                    "M1.1": "M1.1 — Aços inoxidáveis austeníticos (< 700 N/mm²)",
                    "M1.2": "M1.2 — Aços inoxidáveis Duplex (< 1000 N/mm²)",
                    "M2.1": "M2.1 — Aços fundidos austeníticos (< 700 N/mm²)",
                    "M3.1": "M3.1 — Aços fundidos Duplex (< 1000 N/mm²)",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)",
                    "K3.1": "K3.1 — Ferro fundido GJV / Mableável GJM (< 500 N/mm²)",
                    "K3.2": "K3.2 — Ferro fundido GJV / Mableável GJM (> 500 N/mm²)",
                    "N2.1": "N2.1 — Cobre não ligado (< 300 N/mm²)",
                    "N2.2": "N2.2 — Cobre ligado (> 300 N/mm²)",
                    "N2.3": "N2.3 — Latão, bronze (< 1200 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {ext:90, mql:90, ar:0}, f: [0.07, 0.09, 0.12, 0.16, 0.20, 0.24] },
                    "P1.2": { vc: {ext:75, mql:75, ar:0}, f: [0.09, 0.12, 0.15, 0.20, 0.25, 0.30] },
                    "P2.1": { vc: {ext:85, mql:85, ar:0}, f: [0.08, 0.11, 0.19, 0.14, 0.24, 0.28] },
                    "P2.2": { vc: {ext:60, mql:60, ar:0}, f: [0.07, 0.09, 0.15, 0.12, 0.19, 0.22] },
                    "P3.1": { vc: {ext:65, mql:65, ar:0}, f: [0.07, 0.10, 0.13, 0.17, 0.21, 0.25] },
                    "P3.2": { vc: {ext:55, mql:55, ar:0}, f: [0.06, 0.08, 0.14, 0.11, 0.17, 0.21] },
                    "P3.3": { vc: {ext:50, mql:45, ar:0}, f: [0.05, 0.07, 0.09, 0.11, 0.14, 0.16] },
                    "P4.1": { vc: {ext:45, mql:50, ar:0}, f: [0.05, 0.07, 0.09, 0.11, 0.14, 0.17] },
                    "P5.1": { vc: {ext:85, mql:85, ar:0}, f: [0.08, 0.11, 0.19, 0.14, 0.24, 0.28] },
                    "P6.1": { vc: {ext:50, mql:45, ar:0}, f: [0.05, 0.07, 0.09, 0.11, 0.14, 0.17] },
                    "M1.1": { vc: {ext:35, mql:35, ar:0}, f: [0.06, 0.08, 0.14, 0.11, 0.18, 0.21] },
                    "M1.2": { vc: {ext:30, mql:30, ar:0}, f: [0.05, 0.07, 0.12, 0.09, 0.15, 0.18] },
                    "M2.1": { vc: {ext:35, mql:35, ar:0}, f: [0.06, 0.08, 0.14, 0.11, 0.18, 0.21] },
                    "M3.1": { vc: {ext:30, mql:30, ar:0}, f: [0.05, 0.07, 0.12, 0.09, 0.15, 0.18] },
                    "K1.1": { vc: {ext:85, mql:85, ar:85}, f: [0.12, 0.17, 0.24, 0.32, 0.41, 0.49] },
                    "K2.1": { vc: {ext:120, mql:100, ar:120}, f: [0.12, 0.17, 0.22, 0.30, 0.38, 0.45] },
                    "K2.2": { vc: {ext:75, mql:75, ar:0}, f: [0.11, 0.15, 0.20, 0.26, 0.33, 0.39] },
                    "K2.3": { vc: {ext:50, mql:40, ar:0}, f: [0.08, 0.10, 0.17, 0.13, 0.22, 0.26] },
                    "K3.1": { vc: {ext:80, mql:80, ar:0}, f: [0.12, 0.16, 0.28, 0.21, 0.35, 0.42] },
                    "K3.2": { vc: {ext:70, mql:70, ar:0}, f: [0.10, 0.13, 0.22, 0.17, 0.28, 0.33] },
                    "N2.1": { vc: {ext:100, mql:0, ar:0}, f: [0.09, 0.12, 0.15, 0.20, 0.25, 0.30] },
                    "N2.2": { vc: {ext:90, mql:0, ar:0}, f: [0.11, 0.15, 0.20, 0.26, 0.33, 0.39] },
                    "N2.3": { vc: {ext:160, mql:160, ar:120}, f: [0.12, 0.17, 0.24, 0.32, 0.41, 0.49] }
                }
            },
            scd121: {
                linha: 'performance',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'MEGA-Drill-Inox SCD121 (Com Refrig. Interna)',
                diametros: [3.00, 4.50, 6.50, 9.50, 14.00, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P4.1", "P5.1", "P6.1", "M1.1", "M1.2", "M2.1", "M3.1", "K1.1", "K2.1", "K2.2", "K2.3", "K3.1", "K3.2", "N2.1", "N2.2", "N2.3"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P4.1": "P4.1 — Aços inoxidáveis ferríticos e martensíticos",
                    "P5.1": "P5.1 — Aço fundido",
                    "P6.1": "P6.1 — Aços fundidos inoxidáveis",
                    "M1.1": "M1.1 — Aços inoxidáveis austeníticos (< 700 N/mm²)",
                    "M1.2": "M1.2 — Aços inoxidáveis Duplex (< 1000 N/mm²)",
                    "M2.1": "M2.1 — Aços fundidos austeníticos (< 700 N/mm²)",
                    "M3.1": "M3.1 — Aços fundidos Duplex (< 1000 N/mm²)",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)",
                    "K3.1": "K3.1 — Ferro fundido GJV / Mableável GJM (< 500 N/mm²)",
                    "K3.2": "K3.2 — Ferro fundido GJV / Mableável GJM (> 500 N/mm²)",
                    "N2.1": "N2.1 — Cobre não ligado (< 300 N/mm²)",
                    "N2.2": "N2.2 — Cobre ligado (> 300 N/mm²)",
                    "N2.3": "N2.3 — Latão, bronze (< 1200 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {int:100, ext:90, mql:90, ar:0}, f: [0.07, 0.09, 0.12, 0.16, 0.20, 0.24] },
                    "P1.2": { vc: {int:90, ext:75, mql:75, ar:0}, f: [0.09, 0.12, 0.15, 0.20, 0.25, 0.30] },
                    "P2.1": { vc: {int:100, ext:85, mql:85, ar:0}, f: [0.08, 0.11, 0.19, 0.14, 0.24, 0.28] },
                    "P2.2": { vc: {int:70, ext:60, mql:60, ar:0}, f: [0.07, 0.09, 0.15, 0.12, 0.19, 0.22] },
                    "P3.1": { vc: {int:75, ext:65, mql:65, ar:0}, f: [0.07, 0.10, 0.13, 0.17, 0.21, 0.25] },
                    "P3.2": { vc: {int:60, ext:55, mql:55, ar:0}, f: [0.06, 0.08, 0.14, 0.11, 0.17, 0.21] },
                    "P3.3": { vc: {int:60, ext:50, mql:45, ar:0}, f: [0.05, 0.07, 0.09, 0.11, 0.14, 0.16] },
                    "P4.1": { vc: {int:60, ext:45, mql:50, ar:0}, f: [0.05, 0.07, 0.09, 0.11, 0.14, 0.17] },
                    "P5.1": { vc: {int:100, ext:85, mql:85, ar:0}, f: [0.08, 0.11, 0.19, 0.14, 0.24, 0.28] },
                    "P6.1": { vc: {int:60, ext:50, mql:45, ar:0}, f: [0.05, 0.07, 0.09, 0.11, 0.14, 0.17] },
                    "M1.1": { vc: {int:55, ext:35, mql:35, ar:0}, f: [0.06, 0.08, 0.14, 0.11, 0.18, 0.21] },
                    "M1.2": { vc: {int:50, ext:30, mql:30, ar:0}, f: [0.05, 0.07, 0.12, 0.09, 0.15, 0.18] },
                    "M2.1": { vc: {int:55, ext:35, mql:35, ar:0}, f: [0.06, 0.08, 0.14, 0.11, 0.18, 0.21] },
                    "M3.1": { vc: {int:50, ext:30, mql:30, ar:0}, f: [0.05, 0.07, 0.12, 0.09, 0.15, 0.18] },
                    "K1.1": { vc: {int:120, ext:85, mql:85, ar:85}, f: [0.12, 0.17, 0.24, 0.32, 0.41, 0.49] },
                    "K2.1": { vc: {int:160, ext:120, mql:100, ar:120}, f: [0.12, 0.17, 0.22, 0.30, 0.38, 0.45] },
                    "K2.2": { vc: {int:100, ext:75, mql:75, ar:0}, f: [0.11, 0.15, 0.20, 0.26, 0.33, 0.39] },
                    "K2.3": { vc: {int:60, ext:50, mql:40, ar:0}, f: [0.08, 0.10, 0.17, 0.13, 0.22, 0.26] },
                    "K3.1": { vc: {int:90, ext:80, mql:80, ar:0}, f: [0.12, 0.16, 0.28, 0.21, 0.35, 0.42] },
                    "K3.2": { vc: {int:80, ext:70, mql:70, ar:0}, f: [0.10, 0.13, 0.22, 0.17, 0.28, 0.33] },
                    "N2.1": { vc: {int:140, ext:100, mql:0, ar:0}, f: [0.09, 0.12, 0.15, 0.20, 0.25, 0.30] },
                    "N2.2": { vc: {int:120, ext:90, mql:0, ar:0}, f: [0.11, 0.15, 0.20, 0.26, 0.33, 0.39] },
                    "N2.3": { vc: {int:200, ext:160, mql:160, ar:120}, f: [0.12, 0.17, 0.24, 0.32, 0.41, 0.49] }
                }
            },
            scd350: {
                linha: 'basic',
                categoria: 'solid',
                temRefrigInt: false,
                nome: 'ECU-Drill-Uni SCD350 (Sem Refrig. Interna)',
                diametros: [1.00, 1.82, 3.31, 6.03, 10.99, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P5.1", "M1.1", "M1.2", "M2.1", "M3.1", "K2.1", "K2.2", "K2.3"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P5.1": "P5.1 — Aço fundido",
                    "M1.1": "M1.1 — Aços inoxidáveis austeníticos (< 700 N/mm²)",
                    "M1.2": "M1.2 — Aços inoxidáveis ferríticos/austeníticos (Duplex) (< 1000 N/mm²)",
                    "M2.1": "M2.1 — Aços fundidos inoxidáveis/refratários austeníticos (< 700 N/mm²)",
                    "M3.1": "M3.1 — Aços fundidos inoxidáveis ferríticos/austeníticos (Duplex) (< 1000 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {ext:70, mql:70, ar:0}, f: [0.03, 0.05, 0.07, 0.10, 0.16, 0.21] },
                    "P1.2": { vc: {ext:55, mql:55, ar:0}, f: [0.04, 0.06, 0.08, 0.13, 0.20, 0.27] },
                    "P2.1": { vc: {ext:65, mql:65, ar:0}, f: [0.04, 0.05, 0.08, 0.12, 0.18, 0.25] },
                    "P2.2": { vc: {ext:45, mql:45, ar:0}, f: [0.04, 0.05, 0.07, 0.10, 0.15, 0.20] },
                    "P3.1": { vc: {ext:50, mql:50, ar:0}, f: [0.03, 0.05, 0.07, 0.11, 0.17, 0.23] },
                    "P3.2": { vc: {ext:40, mql:40, ar:0}, f: [0.03, 0.04, 0.06, 0.09, 0.14, 0.18] },
                    "P3.3": { vc: {ext:40, mql:35, ar:0}, f: [0.03, 0.04, 0.05, 0.11, 0.11, 0.14] },
                    "P5.1": { vc: {ext:65, mql:65, ar:0}, f: [0.04, 0.05, 0.08, 0.12, 0.18, 0.25] },
                    "M1.1": { vc: {ext:30, mql:30, ar:0}, f: [0.03, 0.04, 0.06, 0.09, 0.14, 0.19] },
                    "M1.2": { vc: {ext:25, mql:25, ar:0}, f: [0.02, 0.03, 0.05, 0.08, 0.12, 0.16] },
                    "M2.1": { vc: {ext:30, mql:30, ar:0}, f: [0.03, 0.04, 0.06, 0.09, 0.14, 0.19] },
                    "M3.1": { vc: {ext:25, mql:25, ar:0}, f: [0.02, 0.03, 0.05, 0.08, 0.12, 0.16] },
                    "K2.1": { vc: {ext:90, mql:75, ar:90}, f: [0.05, 0.07, 0.12, 0.19, 0.30, 0.41] },
                    "K2.2": { vc: {ext:55, mql:55, ar:0}, f: [0.04, 0.07, 0.11, 0.17, 0.26, 0.35] },
                    "K2.3": { vc: {ext:55, mql:55, ar:0}, f: [0.04, 0.07, 0.11, 0.17, 0.26, 0.35] }
                }
            },
            scd351: {
                linha: 'basic',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'ECU-Drill-Uni SCD351 (Com Refrig. Interna)',
                diametros: [1.00, 1.82, 3.31, 6.03, 10.99, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P5.1", "M1.1", "M1.2", "M2.1", "M3.1", "K2.1", "K2.2", "K2.3"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P5.1": "P5.1 — Aço fundido",
                    "M1.1": "M1.1 — Aços inoxidáveis austeníticos (< 700 N/mm²)",
                    "M1.2": "M1.2 — Aços inoxidáveis ferríticos/austeníticos (Duplex) (< 1000 N/mm²)",
                    "M2.1": "M2.1 — Aços fundidos inoxidáveis/refratários austeníticos (< 700 N/mm²)",
                    "M3.1": "M3.1 — Aços fundidos inoxidáveis ferríticos/austeníticos (Duplex) (< 1000 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {int:75, ext:70, mql:70, ar:70}, f: [0.03, 0.05, 0.07, 0.10, 0.16, 0.21] },
                    "P1.2": { vc: {int:70, ext:55, mql:55, ar:55}, f: [0.04, 0.06, 0.08, 0.13, 0.20, 0.27] },
                    "P2.1": { vc: {int:75, ext:65, mql:65, ar:65}, f: [0.04, 0.05, 0.08, 0.12, 0.18, 0.25] },
                    "P2.2": { vc: {int:55, ext:45, mql:45, ar:45}, f: [0.04, 0.05, 0.07, 0.10, 0.15, 0.20] },
                    "P3.1": { vc: {int:55, ext:50, mql:50, ar:50}, f: [0.03, 0.05, 0.07, 0.11, 0.17, 0.23] },
                    "P3.2": { vc: {int:45, ext:40, mql:40, ar:40}, f: [0.03, 0.04, 0.06, 0.09, 0.14, 0.18] },
                    "P3.3": { vc: {int:45, ext:40, mql:35, ar:35}, f: [0.03, 0.04, 0.05, 0.11, 0.11, 0.14] },
                    "P5.1": { vc: {int:75, ext:65, mql:65, ar:65}, f: [0.04, 0.05, 0.08, 0.12, 0.18, 0.25] },
                    "M1.1": { vc: {int:45, ext:30, mql:30, ar:30}, f: [0.03, 0.04, 0.06, 0.09, 0.14, 0.19] },
                    "M1.2": { vc: {int:45, ext:25, mql:25, ar:25}, f: [0.02, 0.03, 0.05, 0.08, 0.12, 0.16] },
                    "M2.1": { vc: {int:45, ext:30, mql:30, ar:30}, f: [0.03, 0.04, 0.06, 0.09, 0.14, 0.19] },
                    "M3.1": { vc: {int:45, ext:25, mql:25, ar:25}, f: [0.02, 0.03, 0.05, 0.08, 0.12, 0.16] },
                    "K2.1": { vc: {int:120, ext:90, mql:75, ar:90}, f: [0.05, 0.07, 0.12, 0.19, 0.30, 0.41] },
                    "K2.2": { vc: {int:75, ext:55, mql:55, ar:55}, f: [0.04, 0.07, 0.11, 0.17, 0.26, 0.35] },
                    "K2.3": { vc: {int:75, ext:55, mql:55, ar:55}, f: [0.04, 0.07, 0.11, 0.17, 0.26, 0.35] }
                }
            },
            scd360: {
                linha: 'basic',
                categoria: 'solid',
                temRefrigInt: false,
                nome: 'SCD360 (ECU-Drill-Steel - Sem Refrig. Interna)',
                diametros: [1.00, 1.82, 3.31, 6.03, 10.99, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P5.1", "K1.1", "K2.1", "K2.2", "K2.3", "K3.1", "K3.2"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P5.1": "P5.1 — Aço fundido",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)",
                    "K3.1": "K3.1 — Ferro fundido esferoidal GJV / Mableável GJM (< 500 N/mm²)",
                    "K3.2": "K3.2 — Ferro fundido esferoidal GJV / Mableável GJM (> 500 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {ext:70, mql:70, ar:0}, f: [0.04, 0.06, 0.08, 0.13, 0.20, 0.27] },
                    "P1.2": { vc: {ext:55, mql:55, ar:0}, f: [0.05, 0.07, 0.11, 0.16, 0.24, 0.33] },
                    "P2.1": { vc: {ext:65, mql:65, ar:0}, f: [0.05, 0.07, 0.10, 0.15, 0.23, 0.31] },
                    "P2.2": { vc: {ext:45, mql:45, ar:0}, f: [0.05, 0.06, 0.13, 0.09, 0.18, 0.25] },
                    "P3.1": { vc: {ext:50, mql:50, ar:0}, f: [0.04, 0.06, 0.14, 0.09, 0.21, 0.28] },
                    "P3.2": { vc: {ext:40, mql:40, ar:0}, f: [0.04, 0.05, 0.12, 0.08, 0.17, 0.23] },
                    "P3.3": { vc: {ext:35, mql:40, ar:0}, f: [0.04, 0.05, 0.06, 0.09, 0.13, 0.18] },
                    "P5.1": { vc: {ext:65, mql:65, ar:0}, f: [0.05, 0.07, 0.15, 0.10, 0.23, 0.31] },
                    "K1.1": { vc: {ext:40, mql:35, ar:0}, f: [0.03, 0.04, 0.09, 0.06, 0.14, 0.19] },
                    "K2.1": { vc: {ext:60, mql:60, ar:60}, f: [0.04, 0.07, 0.12, 0.20, 0.32, 0.44] },
                    "K2.2": { vc: {ext:80, mql:70, ar:80}, f: [0.05, 0.07, 0.12, 0.19, 0.30, 0.41] },
                    "K2.3": { vc: {ext:50, mql:50, ar:0}, f: [0.04, 0.07, 0.11, 0.17, 0.26, 0.35] },
                    "K3.1": { vc: {ext:35, mql:25, ar:0}, f: [0.04, 0.05, 0.08, 0.12, 0.17, 0.23] },
                    "K3.2": { vc: {ext:55, mql:55, ar:0}, f: [0.05, 0.07, 0.11, 0.18, 0.27, 0.38] }
                }
            },
            scd361: {
                linha: 'basic',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'SCD361 (ECU-Drill-Steel - Com Refrig. Interna)',
                diametros: [1.00, 1.82, 3.31, 6.03, 10.99, 20.00],
                gruposList: ["P1.1", "P1.2", "P2.1", "P2.2", "P3.1", "P3.2", "P3.3", "P5.1", "K1.1", "K2.1", "K2.2", "K2.3", "K3.1", "K3.2"],
                gruposNames: {
                    "P1.1": "P1.1 — Aços estruturais, corte livre (< 700 N/mm²)",
                    "P1.2": "P1.2 — Aços estruturais, corte livre (< 1200 N/mm²)",
                    "P2.1": "P2.1 — Aços de têmpera, nitretados (< 900 N/mm²)",
                    "P2.2": "P2.2 — Aços de têmpera, nitretados (< 1400 N/mm²)",
                    "P3.1": "P3.1 — Aços para ferramentas, rolamento (< 800 N/mm²)",
                    "P3.2": "P3.2 — Aços para ferramentas, rolamento (< 1000 N/mm²)",
                    "P3.3": "P3.3 — Aços para ferramentas, rolamento (< 1500 N/mm²)",
                    "P5.1": "P5.1 — Aço fundido",
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "K2.3": "K2.3 — Ferro fundido esferoidal GJS (> 800 N/mm²)",
                    "K3.1": "K3.1 — Ferro fundido esferoidal GJV / Mableável GJM (< 500 N/mm²)",
                    "K3.2": "K3.2 — Ferro fundido esferoidal GJV / Mableável GJM (> 500 N/mm²)"
                },
                grupos: {
                    "P1.1": { vc: {int:75, ext:70, mql:70, ar:70}, f: [0.04, 0.06, 0.08, 0.13, 0.20, 0.27] },
                    "P1.2": { vc: {int:70, ext:55, mql:55, ar:55}, f: [0.05, 0.07, 0.11, 0.16, 0.24, 0.33] },
                    "P2.1": { vc: {int:75, ext:65, mql:65, ar:65}, f: [0.05, 0.07, 0.10, 0.15, 0.23, 0.31] },
                    "P2.2": { vc: {int:55, ext:45, mql:45, ar:45}, f: [0.05, 0.06, 0.13, 0.09, 0.18, 0.25] },
                    "P3.1": { vc: {int:55, ext:50, mql:50, ar:50}, f: [0.04, 0.06, 0.14, 0.09, 0.21, 0.28] },
                    "P3.2": { vc: {int:45, ext:40, mql:40, ar:40}, f: [0.04, 0.05, 0.12, 0.08, 0.17, 0.23] },
                    "P3.3": { vc: {int:45, ext:35, mql:40, ar:40}, f: [0.04, 0.05, 0.06, 0.09, 0.13, 0.18] },
                    "P5.1": { vc: {int:75, ext:65, mql:65, ar:65}, f: [0.05, 0.07, 0.15, 0.10, 0.23, 0.31] },
                    "K1.1": { vc: {int:45, ext:40, mql:35, ar:35}, f: [0.03, 0.04, 0.09, 0.06, 0.14, 0.19] },
                    "K2.1": { vc: {int:80, ext:60, mql:60, ar:60}, f: [0.04, 0.07, 0.12, 0.20, 0.32, 0.44] },
                    "K2.2": { vc: {int:110, ext:80, mql:70, ar:80}, f: [0.05, 0.07, 0.12, 0.19, 0.30, 0.41] },
                    "K2.3": { vc: {int:70, ext:50, mql:50, ar:50}, f: [0.04, 0.07, 0.11, 0.17, 0.26, 0.35] },
                    "K3.1": { vc: {int:40, ext:35, mql:25, ar:25}, f: [0.04, 0.05, 0.08, 0.12, 0.17, 0.23] },
                    "K3.2": { vc: {int:60, ext:55, mql:55, ar:55}, f: [0.05, 0.07, 0.11, 0.18, 0.27, 0.38] }
                }
            },
            scd211: {
                linha: 'basic',
                categoria: 'solid',
                temRefrigInt: true,
                nome: 'ECU-G-Drill SCD211 (Com Refrig. Interna)',
                diametros: [3.00, 4.50, 6.50, 9.50, 14.00, 20.00],
                gruposList: ["K1.1", "K2.1", "K2.2", "N1.2", "N1.3", "N1.4", "N2.3"],
                gruposNames: {
                    "K1.1": "K1.1 — Ferro fundido lamelar GJL (< 300 N/mm²)",
                    "K2.1": "K2.1 — Ferro fundido esferoidal GJS (< 500 N/mm²)",
                    "K2.2": "K2.2 — Ferro fundido esferoidal GJS (≤ 800 N/mm²)",
                    "N1.2": "N1.2 — Alumínio ligado ≤ 7% Si",
                    "N1.3": "N1.3 — Alumínio ligado > 7-12% Si",
                    "N1.4": "N1.4 — Alumínio ligado > 12% Si",
                    "N2.3": "N2.3 — Latão, bronze (< 1200 N/mm²)"
                },
                grupos: {
                    "K1.1": { vc: {int:90, ext:65, mql:65, ar:65}, f: [0.08, 0.12, 0.16, 0.22, 0.29, 0.34] },
                    "K2.1": { vc: {int:120, ext:90, mql:75, ar:90}, f: [0.08, 0.12, 0.16, 0.21, 0.27, 0.32] },
                    "K2.2": { vc: {int:75, ext:55, mql:55, ar:0}, f: [0.08, 0.10, 0.14, 0.18, 0.23, 0.27] },
                    "N1.2": { vc: {int:215, ext:155, mql:170, ar:0}, f: [0.08, 0.10, 0.14, 0.18, 0.23, 0.27] },
                    "N1.3": { vc: {int:185, ext:155, mql:130, ar:0}, f: [0.08, 0.10, 0.14, 0.18, 0.23, 0.27] },
                    "N1.4": { vc: {int:155, ext:100, mql:130, ar:0}, f: [0.08, 0.10, 0.14, 0.18, 0.23, 0.27] },
                    "N2.3": { vc: {int:160, ext:130, mql:130, ar:95}, f: [0.08, 0.12, 0.16, 0.22, 0.29, 0.34] }
                }
            }
        };

        function atualizarFiltroBrocas() {
            const linhaSel = document.getElementById('linha').value;
            const categoriaSel = document.getElementById('categoria').value;
            const refrigSel = document.getElementById('filtro-refrig').value;
            const brocaSelect = document.getElementById('broca');
            
            brocaSelect.innerHTML = '';
            let primeiraChave = null;

            for (const key in dados) {
                const ferramenta = dados[key];
                const matchLinha = ferramenta.linha === linhaSel;
                const matchCat = ferramenta.categoria === categoriaSel;
                const matchRefrig = (refrigSel === 'com' && ferramenta.temRefrigInt) || (refrigSel === 'sem' && !ferramenta.temRefrigInt);

                if (matchLinha && matchCat && matchRefrig) {
                    const opt = document.createElement('option');
                    opt.value = key;
                    opt.text = ferramenta.nome;
                    brocaSelect.appendChild(opt);
                    if (!primeiraChave) primeiraChave = key;
                }
            }

            if (!primeiraChave) {
                const opt = document.createElement('option');
                opt.value = "";
                opt.text = "Nenhuma ferramenta nesta categoria";
                brocaSelect.appendChild(opt);
            }

            mudarBroca();
        }

        function mudarBroca() {
            const brocaKey = document.getElementById('broca').value;
            const grupoSelect = document.getElementById('grupo');
            
            if (!brocaKey || !dados[brocaKey]) return;

            const toolData = dados[brocaKey];
            
            grupoSelect.innerHTML = '';
            toolData.gruposList.forEach((gKey, idx) => {
                const opt = document.createElement('option');
                opt.value = gKey;
                opt.text = toolData.gruposNames[gKey];
                if(idx === 0) opt.selected = true;
                grupoSelect.appendChild(opt);
            });

            const btnInt = document.getElementById('ref-int');
            const avisoRefrig = document.getElementById('aviso-refrig');
            
            if (!toolData.temRefrigInt) {
                btnInt.disabled = true;
                btnInt.className = "py-1.5 rounded bg-slate-800 text-slate-600 cursor-not-allowed";
                avisoRefrig.classList.remove('hidden');
                if (refrigAtual === 'int') {
                    setRefrig('ext');
                }
            } else {
                btnInt.disabled = false;
                avisoRefrig.classList.add('hidden');
                setRefrig('int');
            }

            mudarGrupoMaterial();
        }

        function mudarGrupoMaterial() {
            const grupoKey = document.getElementById('grupo').value;
            if (grupoKey) {
                const densidadeSugerida = getDensidadePadrao(grupoKey);
                document.getElementById('densidade').value = densidadeSugerida;
            }
            atualizarCalculo();
        }

        function setRefrig(tipo) {
            const brocaKey = document.getElementById('broca').value;
            const toolData = dados[brocaKey];
            if (toolData && !toolData.temRefrigInt && tipo === 'int') return;

            refrigAtual = tipo;
            ['int', 'ext', 'mql', 'ar'].forEach(t => {
                const btn = document.getElementById(`ref-${t}`);
                if (toolData && !toolData.temRefrigInt && t === 'int') {
                    btn.disabled = true;
                    btn.className = "py-1.5 rounded bg-slate-800 text-slate-600 cursor-not-allowed";
                    return;
                } else if (t === 'int') {
                    btn.disabled = false;
                }

                if(t === tipo) {
                    btn.className = "py-1.5 rounded bg-blue-600 text-white transition";
                } else {
                    btn.className = "py-1.5 rounded text-slate-400 hover:text-white transition";
                }
            });
            atualizarCalculo();
        }

        function toggleLock(tipo) {
            if (tipo === 'f') {
                fUnlocked = !fUnlocked;
                const input = document.getElementById('input-f');
                const btn = document.getElementById('btn-lock-f');
                const card = document.getElementById('card-f');
                const status = document.getElementById('status-f');
                
                input.readOnly = !fUnlocked;
                if (fUnlocked) {
                    btn.innerText = '🔓';
                    card.className = 'bg-slate-800 p-3 rounded-lg border border-amber-500/80 transition-colors';
                    input.className = 'w-full bg-slate-900 text-xl font-bold text-amber-300 mt-0.5 focus:outline-none rounded px-1 -ml-1 border border-amber-500/40';
                    status.innerText = 'Manual';
                    status.className = 'text-[9px] text-amber-400 font-semibold';
                    input.focus();
                } else {
                    btn.innerText = '🔒';
                    card.className = 'bg-slate-800 p-3 rounded-lg border border-slate-700 transition-colors';
                    input.className = 'w-full bg-transparent text-xl font-bold text-white mt-0.5 focus:outline-none rounded px-1 -ml-1';
                    status.innerText = 'Auto';
                    status.className = 'text-[9px] text-slate-500';
                    atualizarCalculo();
                }
            } else if (tipo === 'vc') {
                vcUnlocked = !vcUnlocked;
                const input = document.getElementById('input-vc');
                const btn = document.getElementById('btn-lock-vc');
                const card = document.getElementById('card-vc');
                const status = document.getElementById('status-vc');
                
                input.readOnly = !vcUnlocked;
                if (vcUnlocked) {
                    btn.innerText = '🔓';
                    card.className = 'bg-slate-800 p-3 rounded-lg border border-amber-500/80 transition-colors';
                    input.className = 'w-full bg-slate-900 text-xl font-bold text-amber-300 mt-0.5 focus:outline-none rounded px-1 -ml-1 border border-amber-500/40';
                    status.innerText = 'Manual';
                    status.className = 'text-[9px] text-amber-400 font-semibold';
                    input.focus();
                } else {
                    btn.innerText = '🔒';
                    card.className = 'bg-slate-800 p-3 rounded-lg border border-slate-700 transition-colors';
                    input.className = 'w-full bg-transparent text-xl font-bold text-white mt-0.5 focus:outline-none rounded px-1 -ml-1';
                    status.innerText = 'Auto';
                    status.className = 'text-[9px] text-slate-500';
                    atualizarCalculo();
                }
            } else if (tipo === 'rpm-max') {
                rpmMaxUnlocked = !rpmMaxUnlocked;
                const input = document.getElementById('input-rpm-max');
                const btn = document.getElementById('btn-lock-rpm-max');
                const card = document.getElementById('card-rpm-max');
                const status = document.getElementById('status-rpm-max');
                
                input.readOnly = !rpmMaxUnlocked;
                if (rpmMaxUnlocked) {
                    btn.innerText = '🔓';
                    card.className = 'bg-slate-800 p-3 rounded-lg border border-amber-500/80 transition-colors';
                    input.className = 'w-full bg-slate-900 text-xl font-bold text-amber-300 mt-0.5 focus:outline-none rounded px-1 -ml-1 border border-amber-500/40';
                    status.innerText = 'Ativo';
                    status.className = 'text-[9px] text-amber-400 font-semibold';
                    input.focus();
                } else {
                    btn.innerText = '🔒';
                    card.className = 'bg-slate-800 p-3 rounded-lg border border-slate-700 transition-colors';
                    input.className = 'w-full bg-transparent text-xl font-bold text-white mt-0.5 focus:outline-none rounded px-1 -ml-1';
                    status.innerText = 'Inativo';
                    status.className = 'text-[9px] text-slate-500';
                    atualizarCalculo();
                }
            }
        }

        function ajustarDiametro(delta) {
            const input = document.getElementById('diametro');
            let val = parseFloat(input.value) + delta;
            if (val < 1) val = 1;
            if (val > 30) val = 30;
            input.value = val.toFixed(2);
            atualizarCalculo();
        }

        function ajustarPct(tipo, delta) {
            if (tipo === 'vc') {
                vcPct += delta;
                if (vcPct < -50) vcPct = -50;
                if (vcPct > 50) vcPct = 50;
                document.getElementById('vc-slider').value = vcPct;
            } else if (tipo === 'f') {
                fPct += delta;
                if (fPct < -50) fPct = -50;
                if (fPct > 50) fPct = 50;
                document.getElementById('f-slider').value = fPct;
            }
            atualizarCalculo();
        }

        function onSliderVc() {
            vcPct = parseInt(document.getElementById('vc-slider').value);
            atualizarCalculo();
        }

        function onSliderF() {
            fPct = parseInt(document.getElementById('f-slider').value);
            atualizarCalculo();
        }

        function resetPct(tipo) {
            if (tipo === 'vc') {
                vcPct = 0;
                document.getElementById('vc-slider').value = 0;
            } else if (tipo === 'f') {
                fPct = 0;
                document.getElementById('f-slider').value = 0;
            }
            atualizarCalculo();
        }

        function onManualInput(tipo) {
            if (tipo === 'vc' && vcUnlocked) {
                atualizarCalculo();
            } else if (tipo === 'f' && fUnlocked) {
                atualizarCalculo();
            } else if (tipo === 'rpm-max' && rpmMaxUnlocked) {
                atualizarCalculo();
            }
        }

        function atualizarCalculo() {
            const brocaKey = document.getElementById('broca').value;
            if (!brocaKey || !dados[brocaKey]) return;
            
            let grupoKey = document.getElementById('grupo').value;
            const ligaCheck = document.getElementById('liga-check').checked;
            const toolData = dados[brocaKey];

            let grupoEfetivoKey = grupoKey;
            if (ligaCheck) {
                const idxAtual = toolData.gruposList.indexOf(grupoKey);
                if (idxAtual !== -1 && idxAtual + 1 < toolData.gruposList.length) {
                    grupoEfetivoKey = toolData.gruposList[idxAtual + 1];
                }
            }

            const grupoObj = toolData.grupos[grupoEfetivoKey];
            if (!grupoObj) return;

            let diametro = parseFloat(document.getElementById('diametro').value);
            if (isNaN(diametro) || diametro <= 0) diametro = 8.00;

            let profundidade = parseFloat(document.getElementById('profundidade').value);
            if (isNaN(profundidade) || profundidade <= 0) profundidade = 25.00;

            let densidade = parseFloat(document.getElementById('densidade').value);
            if (isNaN(densidade) || densidade <= 0) densidade = 7.85;

            let precoSucataKg = parseFloat(document.getElementById('preco-sucata').value);
            if (isNaN(precoSucataKg) || precoSucataKg < 0) precoSucataKg = 0.35;

            const diametrosCat = toolData.diametros;
            const fCatArr = grupoObj.f;

            let idxInf = 0;
            for (let i = 0; i < diametrosCat.length; i++) {
                if (diametrosCat[i] <= diametro) {
                    idxInf = i;
                } else {
                    break;
                }
            }

            let a = 0, b = 0, fBase = 0;
            let estadoTexto = "Dentro do intervalo consecutivo";
            let estadoCor = "text-emerald-400";
            let badgeMetodo = "Interpolação Linear";

            if (idxInf >= diametrosCat.length - 1) {
                idxInf = diametrosCat.length - 2;
                estadoTexto = "Acima da gama máxima (Extrapolação)";
                estadoCor = "text-amber-400";
                badgeMetodo = "Extrapolação Superior";
            } else if (diametro < diametrosCat[0]) {
                idxInf = 0;
                estadoTexto = "Abaixo da gama mínima (Extrapolação)";
                estadoCor = "text-amber-400";
                badgeMetodo = "Extrapolação Inferior";
            }

            const x1 = diametrosCat[idxInf];
            const x2 = diametrosCat[idxInf + 1];
            const y1 = fCatArr[idxInf];
            const y2 = fCatArr[idxInf + 1];

            b = (y2 - y1) / (x2 - x1);
            a = y1 - b * x1;

            fBase = a + b * diametro;
            if (fBase < 0.001) fBase = 0.001;

            let fFinal = fBase * (1 + fPct / 100);

            let vcBase = 100;
            if (grupoObj.vc) {
                vcBase = grupoObj.vc[refrigAtual] !== undefined ? grupoObj.vc[refrigAtual] : (grupoObj.vc['ext'] || 100);
            }
            let vcFinal = vcBase * (1 + vcPct / 100);

            if (!vcUnlocked) {
                document.getElementById('input-vc').value = Math.round(vcFinal);
            } else {
                vcFinal = parseFloat(document.getElementById('input-vc').value) || vcFinal;
            }

            if (!fUnlocked) {
                document.getElementById('input-f').value = fFinal.toFixed(4);
            } else {
                fFinal = parseFloat(document.getElementById('input-f').value) || fFinal;
            }

            let n = diametro > 0 ? Math.round((vcFinal * 1000) / (Math.PI * diametro)) : 0;

            if (rpmMaxUnlocked) {
                const rpmMaxVal = parseFloat(document.getElementById('input-rpm-max').value) || 0;
                if (rpmMaxVal > 0 && n > rpmMaxVal) {
                    n = rpmMaxVal;
                    vcFinal = (n * Math.PI * diametro) / 1000;
                    if (!vcUnlocked) {
                        document.getElementById('input-vc').value = Math.round(vcFinal);
                    }
                    estadoTexto = "Limitado por RPM Máx. da Máquina";
                    estadoCor = "text-amber-400";
                }
            }

            const vf = Math.round(fFinal * n);

            // Cálculos de Tempo e Volume
            const cursoEfetivo = profundidade + (0.3 * diametro);
            const tempoFuroSeg = vf > 0 ? (cursoEfetivo / vf) * 60 : 0;

            const raio = diametro / 2;
            const volumeMm3 = Math.PI * Math.pow(raio, 2) * profundidade;
            const volumeCm3 = volumeMm3 / 1000;

            const tempoMin = tempoFuroSeg / 60;
            const taxaRemocao = tempoMin > 0 ? volumeCm3 / tempoMin : 0;

            // Cálculos de Peso e Sucata
            // Densidade em g/cm³, Volume em cm³ -> Massa em gramas = Volume * Densidade
            const massaGrams = volumeCm3 * densidade;
            const massaKg = massaGrams / 1000;
            const valorSucataFuro = massaKg * precoSucataKg;
            const valorSucata1000 = valorSucataFuro * 1000;

            // Cálculos de Força e Binário
            const kc = getKc(grupoEfetivoKey);
            const forcaFf = 0.5 * kc * diametro * Math.pow(fFinal, 0.7);
            const forcaKgf = forcaFf / 9.81;
            const binarioMc = (kc * Math.pow(diametro, 2) * Math.pow(fFinal, 0.8)) / 8000;

            document.getElementById('res-n').innerText = n;
            document.getElementById('res-vf').innerText = vf;
            document.getElementById('res-tempo').innerHTML = tempoFuroSeg.toFixed(2) + ' <span class="text-sm font-normal text-slate-300">seg</span>';
            document.getElementById('res-curso').innerText = cursoEfetivo.toFixed(2) + ' mm';
            document.getElementById('res-volume').innerHTML = volumeMm3.toFixed(1) + ' <span class="text-sm font-normal text-slate-300">mm³</span> (' + volumeCm3.toFixed(2) + ' cm³)';
            document.getElementById('res-taxa').innerText = taxaRemocao.toFixed(1) + ' cm³/min';
            
            document.getElementById('res-peso').innerHTML = massaKg < 0.001 ? massaGrams.toFixed(2) + ' <span class="text-sm font-normal text-slate-300">g</span>' : massaKg.toFixed(4) + ' <span class="text-sm font-normal text-slate-300">kg</span>';
            document.getElementById('res-peso-g').innerText = massaGrams.toFixed(2) + ' g';
            
            document.getElementById('res-sucata-val').innerHTML = valorSucataFuro.toFixed(4) + ' <span class="text-sm font-normal text-slate-300">€</span>';
            document.getElementById('res-sucata-lote').innerText = valorSucata1000.toFixed(2) + ' € / 1000 furos';

            document.getElementById('res-forca').innerHTML = Math.round(forcaFf).toLocaleString() + ' <span class="text-sm font-normal text-slate-300">N</span>';
            document.getElementById('res-forca-kgf').innerText = Math.round(forcaKgf) + ' kgf';
            document.getElementById('res-binario').innerHTML = binarioMc.toFixed(1) + ' <span class="text-sm font-normal text-slate-300">N·m</span>';

            document.getElementById('val-a').innerText = a.toFixed(4) + " mm/rot";
            document.getElementById('val-b').innerText = b.toFixed(4) + " mm/rot·mm";
            const elEstado = document.getElementById('val-estado');
            elEstado.innerText = estadoTexto;
            elEstado.className = "text-xs font-bold " + estadoCor + " mt-1";
            document.getElementById('badge-metodo').innerText = badgeMetodo;

            document.getElementById('vc-pct-val').innerText = (vcPct > 0 ? "+" : "") + vcPct + "%";
            document.getElementById('f-pct-val').innerText = (fPct > 0 ? "+" : "") + fPct + "%";

            const tbody = document.getElementById('tabela-ref');
            tbody.innerHTML = '';
            for (let i = 0; i < diametrosCat.length; i++) {
                const dCat = diametrosCat[i];
                const fCat = fCatArr[i];
                let nCat = Math.round((vcFinal * 1000) / (Math.PI * dCat));
                if (rpmMaxUnlocked) {
                    const rpmMaxVal = parseFloat(document.getElementById('input-rpm-max').value) || 0;
                    if (rpmMaxVal > 0 && nCat > rpmMaxVal) nCat = rpmMaxVal;
                }
                const vfCat = Math.round(fCat * nCat);
                const tr = document.createElement('tr');
                tr.className = i === idxInf || i === idxInf + 1 ? "bg-blue-900/30 font-medium text-white" : "text-slate-300";
                tr.innerHTML = `
                    <td class="py-1">${dCat.toFixed(2)}</td>
                    <td class="py-1">${fCat.toFixed(2)}</td>
                    <td class="py-1">${nCat}</td>
                    <td class="py-1">${vfCat}</td>
                `;
                tbody.appendChild(tr);
            }

            desenharGrafico(diametrosCat, fCatArr, diametro, fFinal);
        }

        function desenharGrafico(diametros, fArr, dAtual, fAtual) {
            const svg = document.getElementById('svg-grafico');
            svg.innerHTML = '';

            const width = 400;
            const height = 180;
            const pad = 25;

            const minX = diametros[0];
            const maxX = diametros[diametros.length - 1];
            const minY = 0;
            const maxY = Math.max(...fArr) * 1.2;

            function scaleX(x) {
                return pad + (x - minX) / (maxX - minX || 1) * (width - 2 * pad);
            }
            function scaleY(y) {
                return height - pad - (y - minY) / (maxY - minY || 1) * (height - 2 * pad);
            }

            let html = `
                <line x1="${pad}" y1="${height - pad}" x2="${width - pad}" y2="${height - pad}" stroke="#475569" stroke-width="1" />
                <line x1="${pad}" y1="${pad}" x2="${pad}" y2="${height - pad}" stroke="#475569" stroke-width="1" />
            `;

            let polylinePoints = "";
            for (let i = 0; i < diametros.length; i++) {
                const cx = scaleX(diametros[i]);
                const cy = scaleY(fArr[i]);
                polylinePoints += `${cx},${cy} `;
            }
            html += `<polyline fill="none" stroke="#3b82f6" stroke-width="2" points="${polylinePoints}" />`;

            for (let i = 0; i < diametros.length; i++) {
                const cx = scaleX(diametros[i]);
                const cy = scaleY(fArr[i]);
                html += `<circle cx="${cx}" cy="${cy}" r="3" fill="#3b82f6" />`;
            }

            const curX = scaleX(dAtual);
            const curY = scaleY(fAtual);
            html += `<circle cx="${curX}" cy="${curY}" r="4.5" fill="#f97316" stroke="#fff" stroke-width="1.5" />`;

            svg.innerHTML = html;
        }

        window.onload = function() {
            atualizarFiltroBrocas();
        };
    </script>
</body>
</html>
'''

components.html(html_content, height=900, scrolling=False)