using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TubeSubscribe : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        GameObject EH = GameObject.FindWithTag("EventHandler");
        EH.GetComponent<EventsSystem>().AddTube(this.gameObject);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
