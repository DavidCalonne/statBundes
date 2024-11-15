let jsonData; 

const fetchJSON = async () => {
  try {
    const response = await fetch('http://localhost:8000/bundes.json');
    jsonData = await response.json(); 
    return jsonData;
  } catch (error) {
    console.error('Erreur :', error);
  }
};

const displayData = async () => {
    const data = await fetchJSON();
    const tbody = document.querySelector('#table-body');

    Array.from(data).forEach(stat => {
        const tr = document.createElement('tr');
        const tdRank = document.createElement('td')
        const tdLogo = document.createElement('td')
        const tdPossession = document.createElement('td')
        const tdCartons = document.createElement('td')
        const tdFautes = document.createElement('td')
        const tdButs = document.createElement('td')
        const tdButsEncaisses = document.createElement('td')
        const tdPeno = document.createElement('td')
        const tdPenoOk = document.createElement('td')
        const tdDuelsAeriens = document.createElement('td')
        const tdDuelsRemportes = document.createElement('td')
        const tdMatchs = document.createElement('td')
        const tdWins = document.createElement('td')
        const tdDraws = document.createElement('td')
        const tdLosses = document.createElement('td')
        const tdGoals = document.createElement('td')

        tdRank.innerText = stat.rank;
        tdLogo.innerHTML = `<img class="logo_club" crossorigin="anonymous" src=${stat.logo} />${stat.team}`;
        tdMatchs.innerText = stat.focused_stats["nbr_matches"] || '0';
        tdWins.innerText = stat.focused_stats["nbr_wins"] || '0';
        tdDraws.innerText = stat.focused_stats["nbr_draws"] || '0';
        tdLosses.innerText = stat.focused_stats["nbr_losses"] || '0';
        tdGoals.innerText = stat.focused_stats["goals"][0] - stat.focused_stats["goals"][1];

        tdButs.innerText = stat.focused_stats["goals"][0] / stat.focused_stats["nbr_matches"] || '0';
        tdButsEncaisses.innerText = stat.focused_stats["goals"][1] / stat.focused_stats["nbr_matches"] || '0';
        tdPeno.innerText = stat.stats["Penalties"] / stat.focused_stats["nbr_matches"] || '0';
        tdPenoOk.innerText = stat.stats["Penalties transformés"] / stat.focused_stats["nbr_matches"] || '0';
        tdPossession.innerText = `${stat.stats["Possession (%)"]}` / stat.focused_stats["nbr_matches"] + "%"|| '0';
        tdCartons.innerText = stat.stats["Cartons"] / stat.focused_stats["nbr_matches"] || '0';
        tdFautes.innerText = stat.stats["Fautes commises"] / stat.focused_stats["nbr_matches"] || '0';
        tdDuelsAeriens.innerText = stat.stats["Duels aériens remportés"] / stat.focused_stats["nbr_matches"] || '0';
        tdDuelsRemportes.innerText = stat.stats["Duels remportés"] / stat.focused_stats["nbr_matches"] || '0';

        tr.append(
          tdRank, 
          tdLogo,
          tdMatchs, 
          tdWins, 
          tdDraws, 
          tdLosses, 
          tdGoals,
          tdButs, 
          tdButsEncaisses, 
          tdPeno, 
          tdPenoOk, 
          tdPossession, 
          tdCartons, 
          tdFautes,tdDuelsAeriens, 
          tdDuelsRemportes, 
          
        );
        tbody.append(tr);
    })
}
displayData();