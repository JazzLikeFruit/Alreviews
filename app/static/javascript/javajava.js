document.addEventListener("DOMContentLoaded", () => {
	document.querySelectorAll(".listitem").forEach((a) => {
		a.addEventListener("click", () => {
			var itemid = a.dataset.itemid
			document.querySelector(".resultlist").style.display = "none"
			document.querySelector("#albumrating").style.display = "inline"
			const request = new XMLHttpRequest()

			request.open("POST", "/album")

			// Callback function for when request completes
			request.onload = () => {
				const data = JSON.parse(request.responseText)

				var picture = document.createElement("img")
				picture.src = data["images"]
				picture.style = "height:200px; width:200px;"
				document.querySelector("#albumimage").appendChild(picture)

				var albumtitle = document.createElement("h1")
				albumtitle.innerHTML = data["name"]
				document.querySelector("#albumtitle").appendChild(albumtitle)
			}
			// Add data to send with request
			const data = new FormData()
			data.append("itemid", itemid)

			// Send request
			request.send(data)
		})
	})
})
