<!DOCTYPE html> <html lang="zh"> <head> <meta charset="utf-8"/> <title>Markdown在线编辑器 - www.MdEditor.com</title> <link rel="shortcut icon" href="https://www.mdeditor.com/images/logos/favicon.ico" type="image/x-icon"/> </head> <body><h1 id="h1-cb_witness"><a name="cb_witness" class="reference-link"></a><span class="header-link octicon octicon-link"></span>cb_witness</h1><h4 id="h4-compute-minimal-beta-witness-for-answer-sets-of-logic-programs"><a name="Compute minimal beta-witness for answer sets of logic programs" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Compute minimal beta-witness for answer sets of logic programs</h4><h3 id="h3-python3-cb_witness-py-h"><a name="python3 cb_witness.py -h" class="reference-link"></a><span class="header-link octicon octicon-link"></span>python3 cb_witness.py -h</h3><pre class="prettyprint linenums prettyprinted" style=""><ol class="linenums"><li class="L0"><code><span class="pln">usage</span><span class="pun">:</span><span class="pln"> cb_witness</span><span class="pun">.</span><span class="pln">py </span><span class="pun">[-</span><span class="pln">h</span><span class="pun">]</span><span class="pln"> </span><span class="pun">[-</span><span class="pln">file_S FILE_S</span><span class="pun">]</span><span class="pln"> </span><span class="pun">[-</span><span class="pln">MUS_Solver MUS_SOLVER</span><span class="pun">]</span></code></li><li class="L1"><code><span class="pln"> </span><span class="pun">(-</span><span class="pln">TT_OLD </span><span class="pun">|</span><span class="pln"> </span><span class="pun">-</span><span class="pln">TT_SAT </span><span class="pun">|</span><span class="pln"> </span><span class="pun">-</span><span class="pln">TT_PYSAT</span><span class="pun">)</span><span class="pln"> </span><span class="pun">(-</span><span class="pln">orig </span><span class="pun">|</span><span class="pln"> </span><span class="pun">-</span><span class="pln">v2 </span><span class="pun">|</span><span class="pln"> </span><span class="pun">-</span><span class="pln">v3 </span><span class="pun">|</span><span class="pln"> </span><span class="pun">-</span><span class="pln">v4</span><span class="pun">)</span></code></li><li class="L2"><code><span class="pln"> </span><span class="pun">[-</span><span class="pln">WITNESS_OLD</span><span class="pun">]</span><span class="pln"> </span><span class="pun">[-</span><span class="pln">REDUCE</span><span class="pun">]</span><span class="pln"> </span><span class="pun">[-</span><span class="pln">lp</span><span class="pun">]</span><span class="pln"> </span><span class="pun">[-</span><span class="pln">q</span><span class="pun">]</span><span class="pln"> </span><span class="pun">[-</span><span class="pln">t MCT</span><span class="pun">]</span></code></li><li class="L3"><code><span class="pln"> file_CNF file_M</span></code></li></ol></pre><p>positional arguments:</p> <pre class="prettyprint linenums prettyprinted" style=""><ol class="linenums"><li class="L0"><code><span class="pln"> file_CNF theory file</span></code></li><li class="L1"><code><span class="pln"> file_M model file</span></code></li></ol></pre><p>optional arguments:</p> <pre class="prettyprint linenums prettyprinted" style=""><ol class="linenums"><li class="L0"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">h</span><span class="pun">,</span><span class="pln"> </span><span class="pun">--</span><span class="pln">help show </span><span class="kwd">this</span><span class="pln"> help message </span><span class="kwd">and</span><span class="pln"> </span><span class="kwd">exit</span></code></li><li class="L1"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">file_S FILE_S S file</span></code></li><li class="L2"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">MUS_Solver MUS_SOLVER</span></code></li><li class="L3"><code><span class="pln"> MUS solver</span></code></li><li class="L4"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">TT_OLD </span><span class="kwd">use</span><span class="pln"> enumeration algorithm </span><span class="kwd">for</span><span class="pln"> consequence checking</span></code></li><li class="L5"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">TT_SAT </span><span class="kwd">use</span><span class="pln"> sat solver </span><span class="kwd">for</span><span class="pln"> consequence checking </span><span class="pun">(</span><span class="pln">large</span></code></li><li class="L6"><code><span class="pln"> overhead </span><span class="kwd">for</span><span class="pln"> file generation</span></code></li><li class="L7"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">TT_PYSAT </span><span class="kwd">use</span><span class="pln"> pysat </span><span class="kwd">package</span><span class="pln"> </span><span class="kwd">with</span><span class="pln"> glucose4 </span><span class="kwd">for</span><span class="pln"> consequence</span></code></li><li class="L8"><code><span class="pln"> checking</span></code></li><li class="L9"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">orig </span><span class="kwd">use</span><span class="pln"> the original algorithm proposed </span><span class="kwd">in</span><span class="pln"> the original</span></code></li><li class="L0"><code><span class="pln"> paper</span></code></li><li class="L1"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">v2 </span><span class="kwd">use</span><span class="pln"> the second version of the algorithm suited </span><span class="kwd">for</span></code></li><li class="L2"><code><span class="pln"> small minimal witnesses</span></code></li><li class="L3"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">v3 </span><span class="kwd">use</span><span class="pln"> the third version of the algorithm just mentioned</span></code></li><li class="L4"><code><span class="pln"> </span><span class="kwd">in</span><span class="pln"> the thesis</span><span class="pun">.</span><span class="pln"> </span><span class="typ">It</span><span class="pln"> first adds clauses to </span><span class="typ">Sigma_v</span><span class="pln"> </span><span class="kwd">until</span></code></li><li class="L5"><code><span class="pln"> atoms follow </span><span class="kwd">and</span><span class="pln"> </span><span class="kwd">then</span><span class="pln"> removes them </span><span class="kwd">until</span><span class="pln"> just one atom</span></code></li><li class="L6"><code><span class="pln"> </span><span class="kwd">is</span><span class="pln"> the consequence </span><span class="pun">(</span><span class="pln">pair </span><span class="pun">(</span><span class="pln">v</span><span class="pun">,</span><span class="typ">Sigma_v</span><span class="pun">))</span></code></li><li class="L7"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">v4 </span><span class="kwd">use</span><span class="pln"> unit propagation at first </span><span class="kwd">in</span><span class="pln"> each iteration</span></code></li><li class="L8"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">WITNESS_OLD unoptimized version of the algorithm </span><span class="pun">(</span><span class="pln">enumerating over</span></code></li><li class="L9"><code><span class="pln"> all theory subsets </span><span class="kwd">and</span><span class="pln"> </span><span class="kwd">no</span><span class="pln"> theory reducing</span><span class="pun">)</span><span class="pln"> </span><span class="typ">Just</span></code></li><li class="L0"><code><span class="pln"> possible </span><span class="kwd">with</span><span class="pln"> the original version </span><span class="pun">(-</span><span class="pln">orig argument</span><span class="pun">)</span></code></li><li class="L1"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">REDUCE reduce theory every time an atom </span><span class="kwd">is</span><span class="pln"> added to the </span><span class="kwd">set</span><span class="pln"> T</span></code></li><li class="L2"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">lp </span><span class="typ">The</span><span class="pln"> theory file </span><span class="kwd">is</span><span class="pln"> a logic program</span></code></li><li class="L3"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">q be quiet</span></code></li><li class="L4"><code><span class="pln"> </span><span class="pun">-</span><span class="pln">t MCT CPU limit </span><span class="pun">(</span><span class="pln">s</span><span class="pun">)</span></code></li></ol></pre><h2 id="h2-example"><a name="Example" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Example</h2><p>(1) more data/ex-6.*</p> <pre class="prettyprint linenums prettyprinted" style=""><ol class="linenums"><li class="L0"><code><span class="pun">::::::::::::::</span></code></li><li class="L1"><code><span class="pln">data</span><span class="pun">/</span><span class="pln">ex</span><span class="pun">-</span><span class="lit">6.lp</span></code></li><li class="L2"><code><span class="pun">::::::::::::::</span></code></li><li class="L3"><code><span class="pln">p </span><span class="pun">|</span><span class="pln"> r</span><span class="pun">.</span></code></li><li class="L4"><code><span class="pln">p </span><span class="pun">|</span><span class="pln"> q </span><span class="pun">:-</span><span class="pln"> r</span><span class="pun">.</span></code></li><li class="L5"><code><span class="pln">r </span><span class="pun">|</span><span class="pln"> s </span><span class="pun">:-</span><span class="pln"> p</span><span class="pun">.</span></code></li><li class="L6"><code><span class="pln">p </span><span class="pun">:-</span><span class="pln"> q</span><span class="pun">.</span></code></li><li class="L7"><code><span class="pln">q </span><span class="pun">:-</span><span class="pln"> p</span><span class="pun">.</span></code></li><li class="L8"><code><span class="pln">r </span><span class="pun">:-</span><span class="pln"> s</span><span class="pun">.</span></code></li><li class="L9"><code><span class="pln">s </span><span class="pun">:-</span><span class="pln"> r</span><span class="pun">.</span></code></li><li class="L0"><code><span class="pun">::::::::::::::</span></code></li><li class="L1"><code><span class="pln">data</span><span class="pun">/</span><span class="pln">ex</span><span class="pun">-</span><span class="lit">6.m</span></code></li><li class="L2"><code><span class="pun">::::::::::::::</span></code></li><li class="L3"><code><span class="pln">p q r s</span></code></li></ol></pre><p>(2) python3 cb_witness.py -TT_PYSAT -v4 -lp data/ex-6.lp data/ex-6.m</p> <pre class="prettyprint linenums prettyprinted" style=""><ol class="linenums"><li class="L0"><code><span class="pln">YES</span></code></li><li class="L1"><code><span class="pun">[</span><span class="str">'p'</span><span class="pun">,</span><span class="pln"> </span><span class="str">'r'</span><span class="pun">,</span><span class="pln"> </span><span class="str">'q'</span><span class="pun">,</span><span class="pln"> </span><span class="str">'s'</span><span class="pun">]</span></code></li><li class="L2"><code><span class="pln">p</span><span class="pun">:</span></code></li><li class="L3"><code><span class="pln"> p </span><span class="pun">|</span><span class="pln"> r</span><span class="pun">.</span></code></li><li class="L4"><code><span class="pln"> p </span><span class="pun">|</span><span class="pln"> q </span><span class="pun">:-</span><span class="pln"> r</span><span class="pun">.</span></code></li><li class="L5"><code><span class="pln"> p </span><span class="pun">:-</span><span class="pln"> q</span><span class="pun">.</span></code></li><li class="L6"><code><span class="pln">q</span><span class="pun">:</span></code></li><li class="L7"><code><span class="pln"> q </span><span class="pun">:-</span><span class="pln"> p</span><span class="pun">.</span></code></li><li class="L8"><code><span class="pln">r</span><span class="pun">:</span></code></li><li class="L9"><code><span class="pln"> r </span><span class="pun">|</span><span class="pln"> s </span><span class="pun">:-</span><span class="pln"> p</span><span class="pun">.</span></code></li><li class="L0"><code><span class="pln"> r </span><span class="pun">:-</span><span class="pln"> s</span><span class="pun">.</span></code></li><li class="L1"><code><span class="pln">s</span><span class="pun">:</span></code></li><li class="L2"><code><span class="pln"> s </span><span class="pun">:-</span><span class="pln"> r</span><span class="pun">.</span></code></li><li class="L3"><code><span class="lit">3</span><span class="pln"> clauses have head size </span><span class="pun">&gt;=</span><span class="lit">2</span></code></li><li class="L4"><code><span class="typ">Time</span><span class="pun">:</span><span class="pln"> </span><span class="lit">0.047</span><span class="pln"> </span><span class="pun">(</span><span class="pln">s</span><span class="pun">)</span></code></li><li class="L5"><code><span class="typ">Memory</span><span class="pun">:</span><span class="pln"> </span><span class="lit">17.492</span><span class="pln"> </span><span class="pun">(</span><span class="pln">M</span><span class="pun">)</span></code></li></ol></pre><p>(3) more data/causal_sm.*</p> <pre class="prettyprint linenums prettyprinted" style=""><ol class="linenums"><li class="L0"><code><span class="pun">::::::::::::::</span></code></li><li class="L1"><code><span class="pln">data</span><span class="pun">/</span><span class="pln">causal_sm</span><span class="pun">.</span><span class="pln">lp</span></code></li><li class="L2"><code><span class="pun">::::::::::::::</span></code></li><li class="L3"><code><span class="pln">dead </span><span class="pun">:-</span><span class="pln"> shoot</span><span class="pun">.</span></code></li><li class="L4"><code><span class="pln">shoot </span><span class="pun">:-</span><span class="pln"> tails</span><span class="pun">.</span></code></li><li class="L5"><code><span class="pln">head </span><span class="pun">|</span><span class="pln"> tails </span><span class="pun">:-</span><span class="pln"> harvey</span><span class="pun">.</span></code></li><li class="L6"><code><span class="pln">harvey</span><span class="pun">.</span></code></li><li class="L7"><code><span class="pun">::::::::::::::</span></code></li><li class="L8"><code><span class="pln">data</span><span class="pun">/</span><span class="pln">causal_sm</span><span class="pun">.</span><span class="pln">sm</span></code></li><li class="L9"><code><span class="pun">::::::::::::::</span></code></li><li class="L0"><code><span class="pln">harvey dead shoot tails</span></code></li></ol></pre><p>(4)python3 cb_witness.py -TT_PYSAT -v4 -lp data/causal_sm.lp data/causal_sm.sm</p> <pre class="prettyprint linenums prettyprinted" style=""><ol class="linenums"><li class="L0"><code><span class="pln">YES</span></code></li><li class="L1"><code><span class="pun">[</span><span class="str">'dead'</span><span class="pun">,</span><span class="pln"> </span><span class="str">'shoot'</span><span class="pun">,</span><span class="pln"> </span><span class="str">'tails'</span><span class="pun">,</span><span class="pln"> </span><span class="str">'harvey'</span><span class="pun">]</span></code></li><li class="L2"><code><span class="pln">harvey</span><span class="pun">:</span></code></li><li class="L3"><code><span class="pln"> harvey</span><span class="pun">.</span></code></li><li class="L4"><code><span class="pln">tails</span><span class="pun">:</span></code></li><li class="L5"><code><span class="pln"> tails </span><span class="pun">|</span><span class="pln"> head </span><span class="pun">:-</span><span class="pln"> harvey</span><span class="pun">.</span></code></li><li class="L6"><code><span class="pln">shoot</span><span class="pun">:</span></code></li><li class="L7"><code><span class="pln"> shoot </span><span class="pun">:-</span><span class="pln"> tails</span><span class="pun">.</span></code></li><li class="L8"><code><span class="pln">dead</span><span class="pun">:</span></code></li><li class="L9"><code><span class="pln"> dead </span><span class="pun">:-</span><span class="pln"> shoot</span><span class="pun">.</span></code></li><li class="L0"><code><span class="lit">0</span><span class="pln"> clauses have head size </span><span class="pun">&gt;=</span><span class="lit">2</span></code></li><li class="L1"><code><span class="typ">Time</span><span class="pun">:</span><span class="pln"> </span><span class="lit">0.044</span><span class="pln"> </span><span class="pun">(</span><span class="pln">s</span><span class="pun">)</span></code></li><li class="L2"><code><span class="typ">Memory</span><span class="pun">:</span><span class="pln"> </span><span class="lit">17.227</span><span class="pln"> </span><span class="pun">(</span><span class="pln">M</span><span class="pun">)</span></code></li></ol></pre></body> </html>

