using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GunButton : MonoBehaviour
{
    // Start is called before the first
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
    }
    
    public void StartGame() {
        /*if (other.tag == "Player") {
            GameStarted = true;
        }*/
        GameObject.FindGameObjectWithTag("EventHandler").GetComponent<EventsSystem>().StartTargetGame(Random.Range(0.5f, 1.0f));
    }
}
