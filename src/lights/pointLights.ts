import * as THREE from 'three'

export const createPointLights = (
  scene: THREE.Scene,
  lightCount: number,
  lightDistance: number,
  lights: Array<THREE.Light>,
) => {
  for (let i = 0; i < lightCount; i++) {
    // Positions evenly in a circle pointed at the origin
    const light = new THREE.PointLight(0xffffff, 1)
    let lightX = lightDistance * Math.sin(((Math.PI * 2) / lightCount) * i)
    let lightZ = lightDistance * Math.cos(((Math.PI * 2) / lightCount) * i)
    // Create a light
    light.position.set(lightX, lightDistance, lightZ)
    light.lookAt(0, 0, 0)
    scene.add(light)
    lights.push(light)
    // Visual helpers to indicate light positions
    scene.add(new THREE.PointLightHelper(light, 0.5, 0xff9900))
  }
  return lights
}
