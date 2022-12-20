using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AddPickScript : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        GameObject EH = GameObject.FindWithTag("EventHandler");
        EH.GetComponent<EventsSystem>().AddPick(this.gameObject);
        this.gameObject.SetActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
