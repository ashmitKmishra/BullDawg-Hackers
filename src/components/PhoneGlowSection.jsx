import { motion } from 'framer-motion'

const glowVariants = {
  initial: { opacity: 0, scale: 0.9 },
  animate: {
    opacity: 1,
    scale: 1,
    transition: { duration: 1.2, ease: 'easeOut' }
  },
  hover: {
    y: -12,
    rotate: 2,
    transition: { duration: 0.6, ease: 'easeOut' }
  }
}

const phoneVariants = {
  initial: { opacity: 0, scale: 0.95 },
  animate: {
    opacity: 1,
    scale: 1,
    transition: { duration: 1, ease: 'easeOut', delay: 0.2 }
  },
  hover: {
    y: -6,
    transition: { duration: 0.4, ease: 'easeOut' }
  }
}

export default function PhoneGlowSection({ children, className = '', glowClassName = '' }) {
  return (
    <motion.div
      className={`relative flex items-center justify-center ${className}`}
      initial="initial"
      animate="animate"
      whileHover="hover"
    >
      <motion.div
        variants={glowVariants}
        aria-hidden="true"
        className={`pointer-events-none absolute -z-10 rounded-full blur-3xl opacity-70 ${
          glowClassName ||
          'h-[560px] w-[560px] bg-[radial-gradient(circle_at_center,_#a855f7_0%,_#ec4899_45%,_transparent_75%)]'
        }`}
      />
      <motion.div variants={phoneVariants} className="relative z-10">
        {children}
      </motion.div>
    </motion.div>
  )
}
