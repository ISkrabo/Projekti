using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TargetDeath : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void Death() {
        Instantiate(Resources.Load("Prefabs/Target explosion"), transform.position, transform.rotation);
        Instantiate(Resources.Load("Prefabs/Target smoke"), transform.position, transform.rotation);
        Destroy(this.gameObject);
    }
}
