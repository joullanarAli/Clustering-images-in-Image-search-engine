// async function searchImages() {
//             const query = document.getElementById('query').value;
//             const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
//             const data = await response.json();
//             const resultsDiv = document.getElementById('results');
//             resultsDiv.innerHTML = '';

//             for (const [cluster, images] of Object.entries(data.clusters)) {
//                 const clusterDiv = document.createElement('div');
//                 clusterDiv.className = 'cluster';
                
//                 const title = document.createElement('div');
//                 title.className = 'cluster-title';
//                 title.textContent = `Cluster ${cluster}`;
//                 clusterDiv.appendChild(title);
                
//                 const imgContainer = document.createElement('div');
//                 imgContainer.className = 'image-container';
                
//                 images.forEach(imagePath => {
//                     const img = document.createElement('img');
//                     img.src = `../retrieved_faiss/${imagePath}`;
//                     imgContainer.appendChild(img);
//                 });
                
//                 clusterDiv.appendChild(imgContainer);
//                 resultsDiv.appendChild(clusterDiv);
//             }
//         }

async function searchImages() {
    // Correctly get the value of the query input
    const query = document.getElementById('searchQuery').value;
    console.log(query)
    // Get the selected value for the number of clusters
    var clusterSelect = document.getElementById("clusterSelect");
    var n_clusters = clusterSelect.options[clusterSelect.selectedIndex].value;

    // Ensure query value is correctly passed and redirect to results page with parameters
    window.location.href = `../static/results.html?query=${encodeURIComponent(query)}&n_clusters=${n_clusters}`;
}


function showSidebar(){
    const sidebar = document.querySelector('.sidebar')
    sidebar.style.display = 'flex'
}

function hideSidebar(){
    const sidebar = document.querySelector('.sidebar')
    sidebar.style.display = 'none'
}


