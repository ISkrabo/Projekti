using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using BNG;
using System.IO;
using System.Linq;

//glavni sustav za podatke
//blink se dobiva iz TobiiXRCustom
//podatci o metama (pucanje) je iz TargetScript

public class EventsSystem : MonoBehaviour
{
    private float gameCountdown = 60f;
    //numOfBlinks
    public List<float> blinkTimes = new List<float>();  //tobiiXRcustom
    public int shotsFired = 0;
    //shotsAcc
    public List<float> targetFocusTimes = new List<float>();
    public int numOfUnfocused;
    public List<float> targetTimes = new List<float>();
    
    public bool gameStartedCountdown = false;
    private bool gameLock = false;
    public float gameTime = 0f;

    
    public int gamemode = 0;
    public int PnPRound = -1;
    private string PnPString = "";
    private float PnPTimer = 0f;
    public List<GameObject> placeList = new List<GameObject>();
    public List<GameObject> pickList = new List<GameObject>();
    GameObject place = null;
    GameObject pick = null;
    private bool firstPnPwrite = true;

    public List<GameObject> tubesList = new List<GameObject>();
    public List<GameObject> tubesFire = new List<GameObject>();

    public int boxesMissed = 0;

    GameObject gun;
    GameObject target;
    private float targetTimer;
    private float targetTimerLock;
    GameObject camera;
    GameObject timer;
    GameObject button;

    public bool CameraDetector = false;
    private bool setRandom = false;
    private float randomTime = 0f;
    private bool buttonGameStart = false;
    private bool buttonGameLock = false;
    private int correctButton = 0;
    private int incorrectButton = 0;
    private GameObject leftLight;
    private GameObject rightLight;
    bool buttonDone = false;

    string dataTextPath = "Assets/Resources/Data/results.csv"; 
    // dataTextCurrentUser = ""; nadodaje se na kraj dataTextPath-a + ".txt"
    public string dataTextCurrentUser;

    // Start is called before the first frame update
    void Start()
    {
        gun = GameObject.Find("Gun");
        camera = GameObject.FindGameObjectWithTag("MainCamera");
        timer = GameObject.Find("Timer");
        button = GameObject.Find("BOXBUTTON");
        //dataTextPath += dataTextCurrentUser + ".txt";
        leftLight = GameObject.Find("LeftLight");
        rightLight = GameObject.Find("RightLight");
    }

    // Update is called once per frame
    void Update()
    {
        if (gamemode == 1) GunGame();
        else if (gamemode == 2 && PnPRound == 3) 
        {
            button.SetActive(false);
        } 
        else if (gamemode == 3) 
        {
            gameTime += Time.deltaTime;
            SlashGame(gameTime);
        } 
        else if (gamemode == 4 && gameCountdown > 0f) 
        {
            ButtonGame();
        }

        if (PnPRound >= 0 && PnPRound <= 2) {
            PnPTimer += Time.deltaTime;
        }
        if (gamemode == 4 && gameCountdown <= 0f && buttonGameLock) {
            ButtonGame();
        } else if (gamemode == 4 && gameCountdown <= 0f && !buttonDone) {
            buttonDone = true;
            writeData();
        }

    }

    public void StartTargetGame(float spawnDelay) {
        gamemode = 1;
        gameStartedCountdown = true;
        targetTimerLock = spawnDelay;
    }

    private void GunGame() {
        if (gameStartedCountdown) {
            gameCountdown -= Time.deltaTime;
            targetTimer += Time.deltaTime;
            timer.GetComponent<Text>().text = Mathf.Ceil(gameCountdown).ToString();
        }

        if (target == null && targetTimer > targetTimerLock && !gameLock) {
            SpawnTarget();
        }

        if (InputBridge.Instance.RightTriggerDown) {
            gun.GetComponent<GunMechanism>().Shoot();
            if (gameStartedCountdown && gameCountdown > 0) {
                shotsFired++;
            }
        }

        if (gameCountdown < 0 && !gameLock) {
            if (target != null) {
                target.GetComponent<TargetScript>().EndOfGameDeath();
                GameObject bullet = GameObject.Find("Bullet(Clone)");
                Debug.Log(bullet);
                if (bullet != null) shotsFired--;
            }
            gameStartedCountdown = false;
            writeData();
            gameLock = true;
        }
    }

    public void StartPnPGame() {
        gameStartedCountdown = true;
        pickList.Sort((x, y) => x.name.CompareTo(y.name));
        placeList.Sort((x, y) => x.name.CompareTo(y.name));
        gamemode = 2;
        PnPRound++;
        PnPGame();
    }

    private void PnPGame() {

        if (PnPRound > 0 && PnPRound < 4) {
            Vector3 placePos;
            float placeRot;
            float length = place.transform.localScale.x / 2;

            //dohvati podatke od ciljnog mjesta (place)
            placePos = place.transform.position;
            placeRot = place.transform.rotation.eulerAngles.y;
            while (placeRot > 45f) {
                placeRot -= 90f;
            }

            //podaci stavljenog objekta (pick) i izracun preciznosti
            Vector3 pickPos = pick.gameObject.transform.position;
            //usporedjujemo samo X i Z varijable, Y je vertikalna os
            //gledamo koliko je udaljeno od sredista s obzirom na duljinu objekta (polovicna jer gledamo apsolutnu vrijednost)
            float accuracyX = ((length - Mathf.Abs(placePos.x - pickPos.x)) / length) * 100;
            float accuracyZ = ((length - Mathf.Abs(placePos.z - pickPos.z)) / length) * 100;

            //Debug.Log(accuracyX);
            //Debug.Log(accuracyZ);

            PnPString += accuracyX.ToString("F2") + ";" + accuracyZ.ToString("F2") + ";";

            //ne moramo odredjivati koji vektor odredjuje rotaciju objekta, euler angle uvijek vraca relativnu rotaciju Y-osi naspram svijeta
            if (PnPRound < 4) {
                float pickRot = pick.gameObject.transform.rotation.eulerAngles.y;
                while (pickRot > 45f) {
                    pickRot -= 90f;
                }
                float accuracyRot = Mathf.Abs(placeRot - pickRot);
                accuracyRot = (1 - (accuracyRot / 45f)) * 100;
                //Debug.Log("percent " + accuracyRot);
                PnPString += accuracyRot.ToString("F2");
            }

            //Debug.Log(PnPString);

            writeData();

            PnPString = "";
        }
        if (PnPRound > 0 && PnPRound < 4) {
            placeList[PnPRound-1].SetActive(false);
            pickList[PnPRound-1].SetActive(false);
        }

        
        if (PnPRound < 3) {
        place = placeList[PnPRound];
        pick = pickList[PnPRound];
        place.SetActive(true);
        pick.SetActive(true);
        }
    }

    public void StartSlashGame() {
        gamemode = 3;
        gameStartedCountdown = true;
    }

    private void SlashGame(float time) {
        if (time >= 4f && gameCountdown > 1) {
            //spawn
            gameTime = 0;
            int number;
            if (gameCountdown > 40) number = 1;
            else if (gameCountdown > 20) number = 2;
            else number = 3;
            tubesFire = GetRandomItemsFromList<GameObject>(tubesList, number);

            foreach (GameObject x in tubesFire) {
                SpawnBox(x);
            }
        }

        if (gameStartedCountdown) {
            gameCountdown -= Time.deltaTime;
            timer.GetComponent<Text>().text = Mathf.Ceil(gameCountdown).ToString();
        }

        if (gameCountdown < 0 && gameStartedCountdown) {
            gameStartedCountdown = false;
            writeData();
        }
    }

    public void StartButtonGame() {
        gameStartedCountdown = true;
        gamemode = 4;
        setRandom = true;
        buttonGameStart = true;
    }

    private void ButtonGame() {
        if (gameCountdown > 0f) gameCountdown -= Time.deltaTime;
        timer.GetComponent<Text>().text = Mathf.Ceil(gameCountdown).ToString();
        if (!buttonGameLock) {
                if (setRandom) { //random timer za kada ce se upaliti svijetlo
                    setRandom = false;
                    randomTime = Random.Range(2f, 4f);
                }
                if (CameraDetector == true && !setRandom) {
                    if (buttonGameStart) 
                        gameTime += Time.deltaTime; //odbrojava dok korisnik gleda ispravno
                    if (gameTime > randomTime && buttonGameStart) {
                        buttonGameStart = false;
                    }
                    if (gameTime > randomTime && !buttonGameStart) {
                        pickLight();
                        buttonGameLock = true;
                    }
                }
            }
            //gameCountdown;
    }

    public void TargetData(float timeToFocus, float timer, bool hit) {
        if (hit) {
            if (timeToFocus == 0f) numOfUnfocused++;
            else targetFocusTimes.Add(timeToFocus);
        } else if (!hit) {
            boxesMissed++;
        }
        targetTimes.Add(timer);
        targetTimer = 0f;
        targetTimerLock = Random.Range(0.5f, 1.0f);
    }

    public void AddBlink(float blinkDuration) {
        if (gameStartedCountdown) blinkTimes.Add(blinkDuration);
    }
    

    private void SpawnTarget() {
        float x;
        float y; 
        float z = 7.0f;
        Vector3 cameraDirection = camera.GetComponent<Transform>().localRotation.eulerAngles;
        
        x = Random.Range(-3f, 3f);
        //gleda prema gore
        if (cameraDirection.x > 180) {
            //gleda prema lijevo
            if (cameraDirection.y > 180) {
                if (x < 0) y = Random.Range(-3f, 0f);
                else y = Random.Range(-3f, 3f);
            } 
            //gleda prema desno
            else {
                if (x > 0) y = Random.Range(-3f, 0f);
                else y = Random.Range(-3f, 3f);
            }
        }
        //gleda prema dolje 
        else {
            //gleda prema lijevo
            if (cameraDirection.y > 180) {
                if (x < 0) y = Random.Range(0, 3f);
                else y = Random.Range(-3f, 3f);
            } 
            //gleda prema desno
            else {
                if (x > 0) y = Random.Range(0, 3f);
                else y = Random.Range(-3f, 3f);
            }
        }

        target = (GameObject) Instantiate(Resources.Load("Prefabs/Target"), new Vector3(x, y, z), new Quaternion(0f, 0f, 0f, 0f));
        target.transform.LookAt(camera.transform);
    }

    private void writeData() {
        StreamWriter writer = new StreamWriter(dataTextPath, append: true);

        if (gamemode == 1) {
            float blinkAvgDur = sumList(blinkTimes) / (float) blinkTimes.Count;
            float targetFocusAvg = sumList(targetFocusTimes) / (float) targetFocusTimes.Count;
            float targetTimesAvg = sumList(targetTimes) / (float) targetTimes.Count;

            writer.Write(
                System.DateTime.Now + ";" +
                dataTextCurrentUser + ";" +
                "100;" +
                blinkTimes.Count + ";" +
                blinkAvgDur + ";" +
                shotsFired + ";" +
                (targetTimes.Count / (float) (shotsFired) * 100).ToString("F2") + ";" + 
                targetFocusAvg + ";" +
                numOfUnfocused + ";" +
                targetTimesAvg + ";"
            );
        } else if (gamemode == 2) {
            if (firstPnPwrite) {
                writer.Write("200;");
                firstPnPwrite = false;
            }
            float blinkAvgDur = sumList(blinkTimes) / (float) blinkTimes.Count;
            PnPString = blinkTimes.Count + ";" + blinkAvgDur + ";" + PnPString;
            PnPString += ";" + PnPTimer + ";";
            PnPTimer = 0f;
            writer.Write(PnPString);
        } else if (gamemode == 3) {
            float blinkAvgDur = sumList(blinkTimes) / (float) blinkTimes.Count;
            float targetFocusAvg = sumList(targetFocusTimes) / (float) targetFocusTimes.Count;
            float targetTimesAvg = sumList(targetTimes) / (float) targetTimes.Count;

            writer.Write(
                "300;" + 
                blinkTimes.Count + ";" +
                blinkAvgDur + ";" +
                targetFocusAvg + ";" +
                numOfUnfocused + ";" +
                targetTimesAvg + ";" + 
                boxesMissed + ";"
            );
        } else if (gamemode == 4) {
            float blinkAvgDur = sumList(blinkTimes) / (float) blinkTimes.Count;
            float targetFocusAvg = sumList(targetFocusTimes) / (float) targetFocusTimes.Count;
            float targetTimesAvg = sumList(targetTimes) / (float) targetTimes.Count;

            writer.Write(
                "400;" + 
                blinkTimes.Count + ";" + 
                blinkAvgDur + ";" +
                targetFocusAvg + ";" +
                correctButton + ";" + 
                incorrectButton + ";" +
                targetTimesAvg + "\n"
            );
        }

        writer.Close();
    }

    private float sumList(List<float> list) {
        var r = 0f;
        foreach (var i in list) {
            r += i;
        }
        return r;
    }

    public void AddPick(GameObject obj) {
        pickList.Add(obj);
    }
    public void AddPlace(GameObject obj) {
        placeList.Add(obj);
    }

    public void AddTube(GameObject obj) {
        tubesList.Add(obj);
    }

    private void SpawnBox(GameObject tube) {
        Vector3 position = tube.transform.position;
        position.y = 0.7f;
        
        GameObject box = (GameObject) Instantiate(Resources.Load("Prefabs/Box"), position, new Quaternion(0f, 0f, 0f, 0f));
        box.GetComponent<Rigidbody>().AddForce(new Vector3(0, Random.Range(2, 3.5f), 0));
        box.GetComponent<Rigidbody>().velocity = new Vector3(0, Random.Range(2, 3.5f), 0);
        box.GetComponent<Rigidbody>().angularVelocity = new Vector3(Random.Range(-90, 90), Random.Range(-90, 90), Random.Range(-90, 90));
    }

    public static List<T> GetRandomItemsFromList<T> (List<T> list, int number) {
        // this is the list we're going to remove picked items from
        List<T> tmpList = new List<T>(list);
        // this is the list we're going to move items to
        List<T> newList = new List<T>();
    
        // make sure tmpList isn't already empty
        while (newList.Count < number && tmpList.Count > 0)
        {
            int index = Random.Range(0, tmpList.Count);
            newList.Add(tmpList[index]);
            tmpList.RemoveAt(index);
        }
    
        return newList;
    }
    
    private void pickLight() {
        int r = Random.Range(1, 3);
        if (r == 1) {
            leftLight.GetComponent<LightScript>().SetLight(true);
        } else {
            rightLight.GetComponent<LightScript>().SetLight(true);
        }
    }

    public void AddButtonScore(float timerFocus, float timer) {
        if (buttonGameLock) {
            targetFocusTimes.Add(timerFocus);
            targetTimes.Add(timer);
            correctButton++;
            ButtonReset();
        }
    }

    public void AddButtonWrongScore(float timer) {
        if (buttonGameLock) {
            targetTimes.Add(timer);
            incorrectButton++;
            ButtonReset();
        }
    }

    private void ButtonReset() {
        setRandom = true;
        gameTime = 0f;
        buttonGameStart = true;
        buttonGameLock = false;
        leftLight.GetComponent<LightScript>().SetLight(false);
        rightLight.GetComponent<LightScript>().SetLight(false);
    }
}
