import os
import requests
import img2pdf

class Mangadex:
	def __init__(self, id:str) -> None:
		self.id = id
		self.url = f"https://consumet-api-di2e.onrender.com/meta/anilist-manga/read?chapterId={id}&provider=mangadex"
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
		}
		self.data = {
			"status": None,
			"error": None
		}
  
	def fetch(self):
		try:
			self.response = requests.get(self.url, headers=self.headers)
		except Exception as e:
			self.data["status"] = "Failed"
			self.data["error"] = str(e)
			return self.data
		
		return self.download()


	def download(self):
		try:
			images_list = [i["img"] for i in self.response.json()]
			images_data = [requests.get(img).content for img in images_list]
			with open(os.path.join("tmp", f"{self.id}.pdf"), "wb") as file:
				file.write(img2pdf.convert(images_data))
			return True
			
		except Exception:
			try:
				os.remove(os.path.join("tmp", f"{self.id}.pdf"))
			except FileNotFoundError:
				print("The given ID was invalid.")
			return False


			