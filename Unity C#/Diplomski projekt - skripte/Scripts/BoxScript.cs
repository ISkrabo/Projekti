using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Tobii.G2OM;

public class BoxScript : MonoBehaviour, IGazeFocusable
{
    private float timer = 0f;
    private float timeToFocus = 0f;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        timer += Time.deltaTime;

        if (timer >= 3.5f) {
            Death(false);
        }
    }

    public void GazeFocusChanged(bool hasFocus)
    {
        if (timeToFocus == 0f) timeToFocus = timer;
    }

    public void Death(bool hit) {
        Instantiate(Resources.Load("Prefabs/Target explosion"), transform.position, transform.rotation);
        Instantiate(Resources.Load("Prefabs/Target smoke"), transform.position, transform.rotation);
        GameObject.FindGameObjectWithTag("EventHandler").GetComponent<EventsSystem>().TargetData(timeToFocus, timer, hit); //javlja event systemu podatke
        Destroy(this.gameObject);
    }
    private void OnTriggerEnter(Collider other) {
        if (other.tag == "Player") {
            Death(true);
        }
    }
    
    public void EndOfGameDeath() {
        Destroy(this.gameObject);
    }
}
