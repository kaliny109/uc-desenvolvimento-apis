document.getElementById("buscar").addEventListener("click", () => {
    const usuario = document.getElementById("usuario").value;

    fetch(`https://api.github.com/users/${usuario}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Usuário não encontrado");
            }
            return response.json();
        })
        .then(data => {
            document.getElementById("perfil").innerHTML = `
                <img src="${data.avatar_url}" width="100">
                <h3>${data.name || data.login}</h3>
                <p>${data.bio || "Sem bio"}</p>
                <p>Repositórios: ${data.public_repos}</p>
                <a href="${data.html_url}" target="_blank">Ver perfil</a>
            `;
        })
        .catch(error => {
            document.getElementById("perfil").innerHTML = `<p>${error.message}</p>`;
        });
});