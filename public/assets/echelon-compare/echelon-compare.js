/* ── ALG Echelon Comparison — portable component ──
   Reads window.ECHELON_COMPARE_DATA (per-collection, keyed by live data-app slug).
   Hooks the existing ALL FAMILIES filter (.app-tile[aria-pressed]) and mounts the
   comparison block right AFTER #search-results, only when exactly ONE application is filtered.
   Self-contained; no dependency on the page's own render() internals. */
(function () {
  var DATA = window.ECHELON_COMPARE_DATA;
  if (!DATA) return;
  var TIER_ORDER = DATA.tierOrder, GRADE = DATA.grades, APPS = DATA.apps;
  var TC = { ECO:'--ec-eco', PRO:'--ec-pro', 'PROplus':'--ec-pp', A:'--ec-eco', B:'--ec-pro', AB:'--ec-pp' };
  var SHARED = [['best','Best for'],['grade','Grade'],['eff','Efficacy'],['max','Max wattage · output'],
    ['cri','CRI'],['cct','CCT options'],['volt','Voltage'],['__CAT__'],
    ['ctrl','Controls'],['dlcv','DLC listing'],['warr','Warranty · lifetime'],['skus','SKUs in family']];
  var state = { fam: {}, hidden: false, slug: null };

  function cls(t){ return t === 'PRO+' ? 'PROplus' : (t.replace(/[^A-Za-z]/g,'') || 'AB'); }
  function aa(s){ return String(s).replace(/Ⓐ/g, '<span class="ec-aa">Ⓐ</span>'); }
  function famsAt(a,t){ return (a.tiers && a.tiers[t]) || []; }
  function tiersOf(a){ return TIER_ORDER.filter(function(t){ return famsAt(a,t).length; }); }
  function actIdx(slug,t){ return state.fam[slug+':'+t] || 0; }
  function famOf(a,slug,t){ return famsAt(a,t)[actIdx(slug,t)]; }
  function tierBadge(t){ return '<span class="ec-tbadge tb-'+cls(t)+'">'+t+'</span>'; }
  function tierH(t){ return '<span class="ec-tbadge tb-'+cls(t)+'">'+t+'</span>'; }

  function tierCards(a, slug, tiers){
    var conn = tiers.length === 3 ? '→' : 'VS', parts = [];
    tiers.forEach(function(t,i){
      var fams = famsAt(a,t), idx = actIdx(slug,t), v = fams[idx], chips = '';
      if (fams.length > 1){
        chips = '<div class="ec-chips">' + fams.map(function(fm,j){
          return '<span class="ec-chip'+(j===idx?' on':'')+'" data-tier="'+t+'" data-idx="'+j+'">'+aa(fm.fam)+'</span>';
        }).join('') + '</div>';
      }
      parts.push('<div class="ec-tcard t-'+cls(t)+'" style="--ec-tc:var('+(TC[cls(t)]||'--ec-red')+')"><div class="ec-accent"></div><div class="ec-in">'
        + '<div class="ec-top">'+tierBadge(t)+'<span class="ec-grade">'+(GRADE[t]||'')+'</span></div>'
        + chips + '<div class="ec-name">'+aa(v.fam)+'</div><div class="ec-spec">'
        + '<div class="s"><span class="sk">Efficacy</span><span class="sv">'+aa(v.eff)+'</span></div>'
        + '<div class="s"><span class="sk">Max output</span><span class="sv">'+aa(v.max)+'</span></div>'
        + '<div class="s"><span class="sk">Controls</span><span class="sv">'+aa(v.ctrl)+'</span></div>'
        + '<div class="s"><span class="sk">Warranty · lifetime</span><span class="sv">'+aa(v.warr)+'</span></div>'
        + '</div></div></div>');
      if (i < tiers.length-1) parts.push('<div class="ec-conn">'+conn+'</div>');
    });
    return '<div class="ec-tcards">'+parts.join('')+'</div>';
  }

  function changeTable(a, slug, tiers){
    var rows = []; SHARED.forEach(function(r){ if(r[0]==='__CAT__') a.catRows.forEach(function(c){ rows.push([c[0],c[1]]); }); else rows.push(r); });
    function val(t,key){ var v=famOf(a,slug,t); return key==='grade'?GRADE[t]:key==='skus'?String(v.skus):(v[key]!=null?v[key]:'—'); }
    var N=tiers.length, lw=N===3?15:18, aw=N===3?5:8, vw=((100-lw-aw*(N-1))/N).toFixed(2);
    var cols='<col style="width:'+lw+'%">';
    tiers.forEach(function(t,i){ cols+='<col style="width:'+vw+'%">'; if(i<N-1) cols+='<col style="width:'+aw+'%">'; });
    var h='<div class="ec-twrap"><table class="ec-table"><colgroup>'+cols+'</colgroup><thead><tr><th class="th-title">What each tier upgrades</th>';
    tiers.forEach(function(t,i){ h+='<th class="th-tier">'+tierH(t)+'</th>'; if(i<N-1) h+='<th></th>'; });
    h+='</tr></thead><tbody>';
    rows.forEach(function(r){ var key=r[0], label=r[1]; h+='<tr><td class="rk">'+label+'</td>';
      tiers.forEach(function(t,i){ var v=val(t,key), prev=i>0?val(tiers[i-1],key):null, changed=i>0&&prev!==v;
        h+='<td class="val'+(changed?' changed':'')+'">'+aa(v)+'</td>';
        if(i<N-1){ var up=val(tiers[i+1],key)!==v; h+='<td class="arrow"><span class="'+(up?'arr-up':'arr-hold')+'">→</span></td>'; }
      });
      h+='</tr>';
    });
    h+='</tbody></table></div>';
    if(a.note) h+='<div class="ec-flag">FLAG · '+aa(a.note)+'</div>';
    return h;
  }

  function build(slug){
    var a = APPS[slug]; if(!a) return '';
    var tiers = tiersOf(a); if(!tiers.length) return '';
    if (tiers.length < 2){
      return '<div class="ec-hr"></div><div class="ec-bar"><div><span class="ec-title">Single echelon</span>'
        + '<span class="ec-sub">'+aa(a.label)+' · '+tiers[0]+' only</span></div></div>'
        + '<div class="ec-body">'+tierCards(a,slug,tiers)+'</div>'
        + '<div class="ec-note"><div class="nt">No comparison</div><p>This application ships a single echelon ('+tiers[0]+')'
        + (famsAt(a,tiers[0]).length>1?' — use the chips to switch families.':' — no step-up table.')+(a.note?' '+aa(a.note):'')+'</p></div>';
    }
    var toggle='<button class="ec-toggle" data-toggle="1">'+(state.hidden?'SHOW ▼':'HIDE ▲')+'</button>';
    var bar='<div class="ec-bar"><div><span class="ec-title">'+tiers.join(' → ')+' — what changes</span>'
      + '<span class="ec-sub">'+aa(a.label)+' · '+tiers.length+' tiers</span></div>'+toggle+'</div>';
    var body='<div class="ec-body"'+(state.hidden?' hidden':'')+'>'+tierCards(a,slug,tiers)+changeTable(a,slug,tiers)+'</div>';
    return '<div class="ec-hr"></div>'+bar+body;
  }

  function pressedApps(){
    return [].slice.call(document.querySelectorAll('.app-tile[aria-pressed="true"]'))
      .map(function(b){ return b.getAttribute('data-app'); });
  }
  function mountNode(){
    var sr = document.getElementById('fam-results'); if(!sr) return null;
    var m = document.getElementById('ec-mount');
    if(!m){ m=document.createElement('div'); m.id='ec-mount'; m.className='echelon-compare'; sr.parentNode.insertBefore(m, sr.nextSibling); }
    return m;
  }
  function update(){
    var m = mountNode(); if(!m) return;
    var ps = pressedApps();
    if (ps.length === 1 && APPS[ps[0]]){
      if (state.slug !== ps[0]){ state.slug = ps[0]; state.fam = {}; state.hidden = false; }
      m.innerHTML = build(ps[0]);
    } else { state.slug=null; m.innerHTML=''; }
  }

  // event delegation for chips + HIDE toggle
  document.addEventListener('click', function(e){
    var chip = e.target.closest && e.target.closest('.echelon-compare .ec-chip');
    if (chip){ state.fam[state.slug+':'+chip.getAttribute('data-tier')] = +chip.getAttribute('data-idx'); update(); return; }
    var tg = e.target.closest && e.target.closest('.echelon-compare .ec-toggle');
    if (tg){ state.hidden = !state.hidden; update(); return; }
  });

  function init(){
    if(!document.getElementById('fam-results')) return;
    var debounce; var obs = new MutationObserver(function(){ clearTimeout(debounce); debounce=setTimeout(update, 80); });
    obs.observe(document.body, { subtree:true, childList:true, attributes:true, attributeFilter:['aria-pressed'] });
    document.querySelectorAll('.app-tile').forEach(function(b){ b.addEventListener('click', function(){ setTimeout(update, 80); }); });
    update();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
