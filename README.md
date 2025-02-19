## USAGE

> 20 Feb 2025

#### **Prerequisites**  
1. **Install Git**: [Download here](https://git-scm.com/download/win).  
2. **Install Docker Desktop**: [Download here](https://www.docker.com/products/docker-desktop).  
   - Ensure Docker Desktop is **running** before proceeding.  
3. **Verify Installations:**  
   ```powershell
   git --version
   docker --version
   docker compose version
   ```

---

### **Setup & Run**  
#### **1. Clone the Repository**  
Open **PowerShell** and run:  
```powershell
git clone https://github.com/brandenvs/going-deep.git
cd going-deep/app
```

#### **2. Start the Application**  
```powershell
docker compose up -d
```
- This pulls images and runs containers in the background.  
- Check running containers:  
  ```powershell
  docker compose ps
  ```

#### **3. Verify & Access**  
- View logs (if needed):  
  ```powershell
  docker compose logs -f
  ```
- Open the application in a browser at:  
  ```
  http://localhost:PORT
  ```
  *(Replace `PORT` with the correct value from `docker-compose.yml`.)*

---

### **Stop & Clean Up**  
- **Stop containers:**  
  ```powershell
  docker compose down
  ```
- **Remove containers & volumes (if needed):**  
  ```powershell
  docker compose down --volumes
  ```

#### **Troubleshooting**  
- **Port conflicts?** Modify `ports` in `docker-compose.yml`.  
- **Docker issues?** Restart **Docker Desktop** and try again.  
