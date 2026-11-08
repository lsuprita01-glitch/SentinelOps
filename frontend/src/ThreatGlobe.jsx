
import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, Stars, Float, Line } from "@react-three/drei";
import * as THREE from "three";

function Globe() {
  const globe = useRef();
  const rings = useRef();
  const points = useMemo(() => {
    return Array.from({ length: 90 }, () => {
      const phi = Math.acos(2 * Math.random() - 1);
      const theta = Math.random() * Math.PI * 2;
      const r = 1.55;
      return [
        r * Math.sin(phi) * Math.cos(theta),
        r * Math.sin(phi) * Math.sin(theta),
        r * Math.cos(phi)
      ];
    });
  }, []);

  useFrame((state, delta) => {
    if (globe.current) globe.current.rotation.y += delta * 0.12;
    if (rings.current) rings.current.rotation.z += delta * 0.08;
  });

  return (
    <>
      <group ref={globe}>
        <mesh>
          <sphereGeometry args={[1.45, 64, 64]} />
          <meshStandardMaterial
            color="#071d39"
            metalness={0.75}
            roughness={0.32}
            emissive="#06365b"
            emissiveIntensity={0.45}
          />
        </mesh>

        <mesh>
          <sphereGeometry args={[1.46, 48, 48]} />
          <meshBasicMaterial
            color="#36cfff"
            wireframe
            transparent
            opacity={0.16}
          />
        </mesh>

        <mesh>
          <sphereGeometry args={[1.49, 48, 48]} />
          <meshBasicMaterial
            color="#1c8dce"
            side={THREE.BackSide}
            transparent
            opacity={0.12}
          />
        </mesh>

        {points.map((point, index) => (
          <mesh key={index} position={point}>
            <sphereGeometry args={[index % 9 === 0 ? 0.035 : 0.012, 10, 10]} />
            <meshBasicMaterial
              color={index % 9 === 0 ? "#ff526f" : "#53dcff"}
            />
          </mesh>
        ))}
      </group>

      <group ref={rings}>
        <mesh rotation={[Math.PI / 2.5, 0.2, 0]}>
          <torusGeometry args={[1.85, 0.008, 8, 180]} />
          <meshBasicMaterial color="#32cfff" transparent opacity={0.7} />
        </mesh>
        <mesh rotation={[0.7, 1.1, 0.4]}>
          <torusGeometry args={[2.05, 0.006, 8, 180]} />
          <meshBasicMaterial color="#8b72ff" transparent opacity={0.5} />
        </mesh>
        <mesh rotation={[1.3, 0.5, 0.8]}>
          <torusGeometry args={[2.2, 0.004, 8, 180]} />
          <meshBasicMaterial color="#31a9e9" transparent opacity={0.4} />
        </mesh>
      </group>

      <Float speed={2} rotationIntensity={0.2} floatIntensity={0.15}>
        <mesh position={[1.1, 0.6, 1.1]}>
          <sphereGeometry args={[0.055, 16, 16]} />
          <meshBasicMaterial color="#ff526f" />
        </mesh>
      </Float>
    </>
  );
}

function GlobeScene() {
  return (
    <Canvas camera={{ position: [0, 0, 5.5], fov: 42 }}>
      <ambientLight intensity={1.5} />
      <pointLight position={[3, 3, 4]} intensity={35} color="#30caff" />
      <pointLight position={[-4, -2, -3]} intensity={20} color="#765cff" />
      <Stars radius={80} depth={40} count={1800} factor={2} fade speed={0.6} />
      <Globe />
      <OrbitControls
        enablePan={false}
        enableZoom={false}
        autoRotate
        autoRotateSpeed={0.35}
      />
    </Canvas>
  );
}

export default function ThreatGlobe() {
  return (
    <div className="threat-globe">
      <GlobeScene />
    </div>
  );
}

